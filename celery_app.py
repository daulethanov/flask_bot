from celery import Celery
from bots import bot, types

celery = Celery(__name__, broker='redis://redis:6379/0', backend='redis://redis:6379/0', )
celery.conf['CELERY_TIMEZONE'] = 'Asia/Almaty'


@celery.task()
@bot.message_handler(content_types=['text'])
def send_message(title, user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать')
    markup.add(btn1)
    bot.send_message(user_id, title, reply_markup=markup)


@celery.task()
def send_message_to_users(text, token):
    bot.send_message(token, text)

