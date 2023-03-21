from telebot import types, TeleBot
from ..models import Map

from rest_framework.response import Response


def set_context(message: types.Message, bot: TeleBot):
    bot.set_state(message.from_user.id, message.chat.id)

    map_context_text = "Select the map and side you belong to:"

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    map_keys = []
    maps = Map.objects.all()

    map_keys = [x.name for x in maps]

    keyboard.add(*map_keys)

    bot.send_message(
        chat_id=message.chat.id, text=map_context_text, reply_markup=keyboard
    )
    bot.register_next_step_handler(message, process_map_stage, bot=bot)


def process_map_stage(message: types.Message, bot: TeleBot):
    process_map_text = f"{message.text} is chosen.\n\n"
    process_map_text += "Please select side"

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add("CT", "T")

    bot.send_message(
        chat_id=message.chat.id, text=process_map_text, reply_markup=keyboard
    )
    bot.register_next_step_handler(message, process_side_stage, bot=bot)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["chosen_map"] = message.text


def process_side_stage(message: types.Message, bot: TeleBot):
    process_side_text = f"{message.text} is chosen.\n\n"

    process_side_text += "Now u can choose which grenades to use,\n"
    process_side_text += "for selecting grenades press /grenades_set\n"

    bot.send_message(chat_id=message.chat.id, text=process_side_text)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["chosen_side"] = message.text


# переделать на кнопки формат следующий - 4 кнопки означающие гранаты кнопку нажал граната добавилась/удалилась сообщение отредактировалось.
def grenades(message: types.Message, bot: TeleBot):
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["chosen_grenades"] = []
            grenades_text = "To setup grenades to use please enter grenade prefixes.\n"
            grenades_text += "Use space as divider.\n"
            grenades_text += (
                "Example: m f s - molotov, flash and smoke will be used.\n\n"
            )
            grenades_text += "Avaliable grenades:\n"
            grenades_text += " s - smoke\n"
            grenades_text += " f - flash\n"
            grenades_text += " he - high explosive\n"
            grenades_text += " m - molotov\n"

            bot.send_message(chat_id=message.chat.id, text=grenades_text)
            bot.register_next_step_handler(message, process_grenades, bot)
    except:
        bot.send_message(message.chat.id, text="context is missing")


def process_grenades(message: types.Message, bot: TeleBot):
    grenades = {"s": "SMOKE", "f": "FLASH", "he": "HE", "m": "MOLY"}

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["chosen_grenades"] = [grenades[x] for x in message.text.strip().split(" ")]
        chosen_grenades = data["chosen_grenades"]

        process_grenades_text = "Grenades "
        process_grenades_text += " ".join(chosen_grenades).lower()
        process_grenades_text += " are chosen."

        bot.send_message(chat_id=message.chat.id, text=process_grenades_text)


def get_context(message: types.Message, bot: TeleBot):
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            chosen_map = data["chosen_map"]
            chosen_side = data["chosen_side"]
            chosen_grenades = data["chosen_grenades"]

            get_context_text = (
                f"{chosen_map} {chosen_side} {chosen_grenades} is a context."
            )
            bot.send_message(chat_id=message.chat.id, text=get_context_text)
    except:
        bot.send_message(message.chat.id, text="context is missing")
