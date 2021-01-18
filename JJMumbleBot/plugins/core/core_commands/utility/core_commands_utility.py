from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import C_PLUGIN_TYPE, P_CTR_PLUGIN


def plugin_is_controllable(plugin_name):
    # Iterate through all the registered plugin and search for a match.
    for name, plugin in gs.bot_plugins.items():
        if name == plugin_name:
            # Retrieve the plugin metadata by searching the core plugins first.
            plugin_metadata = PluginUtilityService.process_metadata(f'plugins/core/{name}')
            if C_PLUGIN_TYPE not in plugin_metadata:
                # If the plugin isn't a core plugin, check the extension plugins.
                plugin_metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{name}')
                if C_PLUGIN_TYPE not in plugin_metadata:
                    # If the plugin is neither core or extension, return False.
                    return False, plugin
            # Check the metadata for ControllablePlugin parameter
            is_controllable = plugin_metadata.getboolean(C_PLUGIN_TYPE, P_CTR_PLUGIN)
            if is_controllable:
                return True, plugin
            return False, plugin
    return False, None


def turn_off_plugin(plugin_name):
    plugin_data = plugin_is_controllable(plugin_name)
    if plugin_data[0]:
        plugin_data[1].stop()
        return True
    return False


def turn_on_plugin(plugin_name):
    plugin_data = plugin_is_controllable(plugin_name)
    if plugin_data[0]:
        plugin_data[1].start()
        return True
    return False


def restart_plugin(plugin_name):
    plugin_data = plugin_is_controllable(plugin_name)
    if plugin_data[0]:
        plugin_data[1].stop()
        plugin_data[1].start()
        return True
    return False
