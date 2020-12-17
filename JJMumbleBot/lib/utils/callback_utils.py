from JJMumbleBot.settings.global_settings import plugin_callbacks


def get_callbacks(plugin_name: str):
    clbks = []
    if not plugin_name:
        return clbks
    for clbk in plugin_callbacks:
        split_clbk = clbk.split('|')
        if split_clbk[0] == plugin_name:
            clbks.append(plugin_callbacks[clbk])


def get_callback(plugin_name: str, method_name: str):
    if not plugin_name or not method_name:
        return None
    for clbk in plugin_callbacks:
        split_clbk = clbk.split('|')
        if split_clbk[0] == plugin_name and split_clbk[1] == method_name:
            return plugin_callbacks[clbk]
