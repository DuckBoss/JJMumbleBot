import JJMumbleBot.core.bot_service as service
import JJMumbleBot.settings.global_settings as global_settings
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support "
                    "for custom plugins."
    )
    parser._action_groups.pop()
    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    required_args.add_argument('-ip', dest='server_ip', default='127.0.0.1',
                               required=True,
                               help='Enter the server IP using this parameter.')
    required_args.add_argument('-port', dest='server_port', default='64738',
                               required=True,
                               help='Enter the server port using this parameter.')

    optional_args.add_argument('-password', dest='server_password', default='',
                               help='Enter the server password using this parameter.')
    optional_args.add_argument('-safe', dest='safe_mode', action='store_true', default=False,
                               help='Enables safe mode for the bot service which initializes the bot with safe-mode only '
                                    'plugins.')
    optional_args.add_argument('-verbose', dest='verbose_mode', action='store_true', default=False,
                               help='Enables verbose mode which displays extensive output statements from the bot service. '
                                    'This is useful for debugging purposes.')
    optional_args.add_argument('-quiet', dest='quiet_mode', action='store_true', default=False,
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
    service.BotService(args.server_ip, int(args.server_port), args.server_password)
