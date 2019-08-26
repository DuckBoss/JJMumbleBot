import JJMumbleBot.core.bot_service as service
import JJMumbleBot.core.cla_classifier as cla


if __name__ == "__main__":
    # Check and classify system arguments.
    cla.classify()
    # Initialize bot service.
    service.BotService()
