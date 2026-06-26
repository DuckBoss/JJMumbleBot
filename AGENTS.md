# AGENTS.md

Guidance for AI coding agents working in the **JJMumbleBot** repository.

> **Project status:** This codebase is in maintenance mode. Active development has
> moved to the rewrite, [Mumimo](https://github.com/DuckBoss/Mumimo). Keep the
> legacy bot functional for existing users; do not introduce large architectural
> changes here unless explicitly requested.

---

## 1. What this project is

JJMumbleBot is a plugin-based [Mumble](https://www.mumble.info/) voice-server bot
written in **Python 3.9+**. Users issue text commands in the Mumble channel (e.g.
`!echo`, `!ytplay <url>`) and the bot reacts — playing audio, posting HTML
"GUI" messages, administering the server, etc. It also ships an optional Flask web
interface.

The single most important thing to understand before changing anything is the
**plugin system**, documented in section 4.

---

## 2. Layout

```
.
├── __main__.py                  # Entry point: argparse, env setup, bootstrap
├── docker-compose.yaml / Dockerfile
├── requirements/                # requirements.txt + web_server.txt
└── JJMumbleBot/                 # The actual package
    ├── core/                    # bot_service.py, callback_service.py (main loop)
    ├── lib/                     # Framework internals (NOT plugins)
    │   ├── plugin_template.py   # PluginBase ABC (start/stop/quit)
    │   ├── command.py           # Command dataclass
    │   ├── execute_cmd.py       # Dispatches a command to a plugin callback
    │   ├── privileges.py        # User privilege levels + checks
    │   ├── helpers/             # bot_service_helper.py = plugin loader/init
    │   ├── audio/               # audio_api.py, audio_interface.py
    │   ├── utils/               # dir_utils, logging_utils, plugin_utils, etc.
    │   └── resources/strings.py # Shared string/section-name constants
    ├── plugins/
    │   ├── core/                # Built-in plugins (cannot be removed)
    │   └── extensions/          # Optional feature plugins
    ├── cfg/                     # Runtime config (generated; gitignored)
    ├── settings/                # global_settings.py (runtime globals), runtime_settings.py
    ├── templates/               # Config + plugin scaffolding templates
    └── tests/                   # Framework-level tests
```

`JJMumbleBot/settings/global_settings.py` holds **mutable module-level globals**
(the mumble instance, gui service, loaded plugins, callback registries, config).
It is imported almost everywhere, conventionally as `gs`. It is internal state —
read from it, but do not repurpose it.

---

## 3. Running, testing, building

```bash
# Run (from repo root; the package is executed as a module via __main__.py)
python . -ip <server_ip> -port <port> [-password <pw>]
# Env vars MUMBLE_IP / MUMBLE_PORT / MUMBLE_PASSWORD work as an alternative.
# Useful flags: -safe (safe mode), -quiet, -verbose, -generatecerts, -wb (web interface)

# Tests (pytest is configured in pytest.ini; testpaths = JJMumbleBot)
pytest

# Lint / security (CI uses bandit; config in .bandit)
bandit -r JJMumbleBot

# Docker
docker compose up --build      # reads MUMBLE_IP/PORT/PASSWORD from the environment
```

Dependencies live in `requirements/requirements.txt` (core) and
`requirements/web_server.txt` (Flask web interface). System deps for audio:
`ffmpeg`, `vlc`, `libopus`.

---

## 4. The plugin system (read this before adding a command)

### Plugin types and discovery
- **Core plugins** live in `JJMumbleBot/plugins/core/<name>/`. **Extension
  plugins** live in `JJMumbleBot/plugins/extensions/<name>/`.
- At startup, `lib/helpers/bot_service_helper.py` scans each directory, and loads
  a plugin **only if its folder name is listed in the `safe_mode` plugin list in
  the config** and the folder contains a `metadata.ini`.
- Each plugin folder is dynamically imported as `<name>.<name>` and the loader
  instantiates the class named **`Plugin`** from `<name>/<name>.py`. So the module
  filename, the folder name, and the metadata must all agree.

### Required files in a plugin folder
| File | Purpose |
| --- | --- |
| `<name>.py` | Module containing `class Plugin(PluginBase)`. Filename **must** equal the folder name. |
| `metadata.ini` | Plugin info, settings, type, and the authoritative command list. |
| `privileges.csv` | `command,level` — minimum privilege per command. |
| `aliases.csv` | `alias,command` — default command aliases. |
| `help.html` | HTML help text shown by the help command / web UI. |
| `resources/strings.py` | Plugin-local string constants (optional but conventional). |
| `tests/` | pytest tests for the plugin (see section 5). |
| `utility/`, `resources/` | Optional helper code and assets. |

### How commands are wired
1. `metadata.ini` `[Plugin Information] PluginCommands` is a JSON array of command
   names, e.g. `["coinflip", "customroll"]`.
2. For each command `X` in that list, the loader registers a callback and looks up
   the method **`cmd_X(self, data)`** on the plugin instance.
3. **The contract: every command in `PluginCommands` must have a matching
   `cmd_<command>` method, and vice versa.** Plugin tests assert this equality —
   if you add a command, update the metadata list, the method, `privileges.csv`,
   and `help.html` together.
4. At runtime, `execute_cmd.execute_command` resolves the command to its plugin,
   checks the user's privilege level, then runs `cmd_<command>` either inline
   (`UseSingleThread = True`) or in a worker thread. Commands listed in
   `ThreadWaitForCommands` cause the core loop to `join()` (use this for
   multi-step command sequences like search→play).

### `cmd_<command>(self, data)` conventions
- `data.message` — the full raw message (`!customroll 3 6`). Split it yourself to
  get arguments.
- `data.command` — the command name without the token.
- Post output to the channel via `gs.gui_service.quick_gui(...)` using the
  HTML pseudo-GUI (e.g. `text_type='header'`, `box_align='left'`). Do not `print`.
- Log via `lib.utils.logging_utils.log(LEVEL, msg, origin=..., print_mode=...)`.
  Use the `L_*` origin and `PrintMode` constants, not literals.

### PluginBase lifecycle (`lib/plugin_template.py`)
Every plugin subclasses `PluginBase` and must implement `start`, `stop`, `quit`.
Follow the existing pattern: `__init__` loads metadata and sets `self.is_running`;
`stop()` calls `quit()`; `start()` re-runs `__init__` when stopped. Optionally
implement `register_callbacks()` for event-driven hooks (see the media plugin).

### Adding a new plugin — checklist
1. Scaffold from `JJMumbleBot/templates/plugin_templates/` (`plugin_template.py`,
   `metadata_template.ini`). Note the template's metadata path string uses
   `plugins/extensions/...`; fix it to `plugins/core/...` for a core plugin.
2. Create `plugins/extensions/<name>/<name>.py` with `class Plugin(PluginBase)`.
3. Set the `[Plugin Type]` flags in `metadata.ini` (`ExtensionPlugin = True` /
   `CorePlugin = True`, plus `AudioPlugin`/`ImagePlugin`/`ControllablePlugin` as
   needed) and list every command in `PluginCommands`.
4. Add `privileges.csv`, `aliases.csv`, `help.html`.
5. Add the folder name to the config's `safe_mode` plugin list so it loads.
6. Add a `tests/` module mirroring `randomizer/tests/`.

---

## 5. Testing conventions

- Tests live both in `JJMumbleBot/tests/` (framework) and in each plugin's
  `tests/` folder. They run under `pytest` (see `pytest.ini`, `conftest.py`).
- Plugin tests typically read the plugin's `metadata.ini` directly and assert:
  - the declared `PluginVersion`,
  - the number of commands in `PluginCommands`,
  - that the count of `cmd_*` methods on `Plugin` equals the command count.
- **When you change a plugin's command set or version, update its tests too** —
  these counts are hard-coded and will otherwise fail.

---

## 6. Conventions & guardrails

- **Imports are absolute from the package root**: `from JJMumbleBot.lib...`.
- **Strings/constants**: section names and message strings come from
  `lib/resources/strings.py` (`C_*` config sections, `P_*` property keys, `L_*`
  log origins, `INFO`/`ERROR`/etc.). Reuse them; don't hardcode `"[Plugin Information]"`.
- **No print debugging in plugins** — use the `log(...)` service and `quick_gui`
  for user-facing output.
- **Privileges**: gate destructive/admin commands behind appropriate levels in
  `privileges.csv` (4 = admin in existing plugins; `BLACKLIST` is the floor).
- **Config & generated files** (`cfg/`, `*.db`, logs) are runtime artifacts and
  gitignored — don't commit them. Edit `templates/` to change defaults.
- **Versioning**: bump `PluginVersion` in `metadata.ini` when changing a plugin,
  and update `CHANGELOG.md` for user-visible changes. Keep `__main__.py` arg
  behavior and env-var fallbacks intact.
- Keep new code consistent with the surrounding plugin's style (logging density,
  naming, the `cmd_` prefix). Match what's already there.

---

## 7. Where to look first

- Reference plugin (simple, self-contained): `plugins/extensions/randomizer/`.
- Command dispatch & threading: `lib/execute_cmd.py`.
- Plugin loading/registration: `lib/helpers/bot_service_helper.py`.
- Privilege model: `lib/privileges.py`.
- Audio pipeline: `lib/audio/audio_api.py` + `plugins/core/audio_commands/`.
- Web interface: `plugins/core/web_server/` (Flask routes under `routing/`).
- Full user/developer docs: the project Wiki (linked from `README.md`).
