import JJMumbleBot.settings.global_settings as GS


def dprint(msg):
    if GS.verbose_mode and not GS.quiet_mode:
        print(msg)


def rprint(msg):
    if not GS.quiet_mode:
        print(msg)
