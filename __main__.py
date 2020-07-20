import JJMumbleBot.core.bot_service as service
import JJMumbleBot.settings.global_settings as global_settings
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support "
                    "for custom plugins."
    )
    parser.add_argument('-safe', dest='debug_mode', action='store_true', default=False,
                        help='Enables safe mode for the bot service which initializes the bot with safe-mode only '
                             'plugins.')
    parser.add_argument('-verbose', dest='verbose_mode', action='store_true', default=False,
                        help='Enables verbose mode which displays extensive output statements from the bot service. '
                             'This is useful for debugging purposes.')
    parser.add_argument('-quiet', dest='quiet_mode', action='store_true', default=False,
                        help='Enables quiet mode which suppresses output statements from the bot service. This is '
                             'useful for running the bot in a headless environment.')

    args = parser.parse_args()
    if args.quiet_mode:
        global_settings.quiet_mode = True
    if args.safe_mode:
        global_settings.safe_mode = True
    elif args.verbose_mode:
        global_settings.verbose_mode = True

    if global_settings.verbose_mode and global_settings.quiet_mode:
        from JJMumbleBot.lib.errors import SysArgError
        raise SysArgError("It looks like both verbose mode and quiet mode are enabled. "
                          "Only one or the other can be used!\n")
    # Initialize bot service.
    service.BotService()
