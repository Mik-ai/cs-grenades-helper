from django.shortcuts import render
from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
import time

from .handlers import handlers_register


TG_TOKEN = ""
WEB_HOOK_URL = ""

state_storage = StateMemoryStorage()

bot = TeleBot(TG_TOKEN, state_storage=state_storage)

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=WEB_HOOK_URL)
types.ReplyKeyboardRemove()


class UpdateBot(APIView):
    def post(self, request):
        json_str = request.body.decode("UTF-8")
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({"code": 200})



handlers_register.register(bot)

def test_handler(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, text="test")

bot.register_message_handler(test_handler, commands=["test"], pass_bot=True)
