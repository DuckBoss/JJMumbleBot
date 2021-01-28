from JJMumbleBot.templates.plugin_templates.plugin_template import Plugin


class TestPluginTemplate:
    def setup_method(self):
        pass

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == 1
