from tgcsgrenadebot.models import Map, Grenade
from telebot import TeleBot, types

from rest_framework.response import Response


def start_message(message: types.Message, bot: TeleBot):
    # User написал /start в диалоге с ботом
    text = "Hello welcome to cs grenade bot!\n\n"
    text += "To start using it, you need to fill context to do so press /context.\n\n"
    text += "Available commands:\n"
    text += "/context - setup context for current match\n"
    text += "\n"

    bot.send_message(message.chat.id, text=text)


def get_grenades(message: types.Message, bot: TeleBot):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        chosen_map = data["chosen_map"]
        chosen_side = data["chosen_side"]
        chosen_grenades = data["chosen_grenades"]

        if chosen_map is None or chosen_side is None:
            pass

        cs_go_map_id = Map.objects.get(name=chosen_map).id

        grenades = Grenade.objects.filter(
            map=cs_go_map_id,
            side=chosen_side,
            grenade_type__in=chosen_grenades,
        ).select_related()

        for grenade in grenades:
            bot.send_photo(
                message.chat.id,
                caption=f"{grenade.name}",
                photo=grenade.image_example,
            )


def help(message: types.Message, bot: TeleBot):
    try:
        get_grenades(message, bot)
    except:
        bot.send_message(message.chat.id, text="context is missing")
