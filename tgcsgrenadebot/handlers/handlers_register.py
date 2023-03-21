from telebot import TeleBot, types
from . import main_commands
from . import context_handlers


def register_context_handlers(bot: TeleBot):
    bot.register_message_handler(
        context_handlers.set_context, commands=["context"], pass_bot=True
    )
    bot.register_message_handler(
        context_handlers.grenades, commands=["grenades_set"], pass_bot=True
    )
    bot.register_message_handler(
        context_handlers.get_context, commands=["get_context"], pass_bot=True
    )



def register_main_handlers(bot: TeleBot):
    bot.register_message_handler(
        main_commands.start_message, commands=["start"], pass_bot=True
    )
    bot.register_message_handler(main_commands.help, commands=["help"], pass_bot=True)


def register(bot: TeleBot):
    register_context_handlers(bot)
    register_main_handlers(bot)


