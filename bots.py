import os
from datetime import datetime, timedelta
import telebot
from telebot import types
import logging
from flask_bot.model.ticket import Ticket, db
from flask_bot.model.user import User


token = os.environ.get('BOT_ID')
bot = telebot.TeleBot(token=token)

logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    from app import app
    with app.app_context():
        user = User.query.filter_by(token=user_id).first()
        if user:
            bot.send_message(message.chat.id, 'Вы авторизированный пользователь')
        else:
            bot.send_message(message.chat.id, 'Доступ запрещен')


@bot.message_handler(content_types=['text'])
def start_ticket(message):
    if message.text == 'Начать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Завершить')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Время пошло ...', reply_markup=markup)

    if message.text == 'Завершить':
        from app import app
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ждать следующие задание')
        markup.add(btn1)
        with app.app_context():
            ticket_id = message.chat.id
            ticket = Ticket.query.filter_by(user_id=ticket_id).first()
            ticket.completed_ticket = datetime.now() + timedelta(hours=6)
            ticket.status = True
            db.session.commit()
        bot.send_message(chat_id=ticket_id, text='Тикет отправлен', reply_markup=markup)



if __name__ == '__main__':
    bot.polling()
