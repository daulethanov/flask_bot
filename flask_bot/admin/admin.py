import os
from datetime import datetime, timedelta
import pytz
from flask import flash
from flask_admin.actions import action
from flask_admin import Admin
from flask_login import current_user
from sqlalchemy import func
from celery_app import send_message, send_message_to_users
from . import MyModelView, MyModelViewTicket
from ..model.user import User, Role
from ..model.ticket import Ticket, UserMessage
from ..model import db

admin = Admin()


class UserAdminView(MyModelView):
    column_hide_backrefs = False
    column_list = ('email', 'username', 'token', 'active', 'created_at', 'ticket', 'roles',)


class MyTicketAdminView(MyModelView):
    column_hide_backrefs = False
    column_list = ('username', 'created_at', 'title', 'description')


class MyTicket(MyModelViewTicket):
    column_list = [
        'user_id',
        'title',
        'description',
        'create_at',
        'completed_ticket',
        'status',
    ]

    def get_query(self):
        return self.session.query(self.model).filter(self.model.user_id == current_user.token)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.user_id == current_user.token)

    can_create = False


class TelegramMessage(MyModelView):
    column_list = [
        'user_id',
        'title',
        'description',
        'create_at',
        'completed_ticket',
        'notification_time',
        'status',
    ]

    @action('Запустить рассылку', 'Запустить рассылку', 'Вы уверены, что хотите отправить выбранные сообщения?')
    def action_send_message(self, ids):
        from flask_bot.model.ticket import Ticket, db
        try:
            local_tz = pytz.timezone('Asia/Almaty')
            messages = Ticket.query.filter(Ticket.id.in_(ids)).all()
            for message in messages:
                send_at = message.notification_time.astimezone(local_tz)
                now = datetime.now(tz=local_tz) + timedelta(hours=6)
                if send_at >= now:
                    delay = (send_at - now).total_seconds()
                    send_message.apply_async(args=[message.title, message.user_id], countdown=delay)
                else:
                    send_message.apply_async(args=[message.title, message.user_id])

            flash('Отправлено', 'success')
        except Exception as ex:
            flash(str(ex), 'error')


class TelegramMessageView(MyModelView):
    column_list = ('id', 'text', 'send_time')

    @action('Запустить рассылку', 'Запустить рассылку', 'Вы уверены, что хотите отправить выбранные сообщения?')
    def action_sends_messages(self, ids):
        try:
            local_tz = pytz.timezone('Asia/Almaty')
            messages = UserMessage.query.filter(UserMessage.id.in_(ids)).all()
            for message in messages:
                users = User.query.all()
                for user in users:
                    send_at = message.send_time.astimezone(local_tz)
                    now = datetime.now(tz=local_tz) + timedelta(hours=6)
                    if send_at >= now:
                        delay = (send_at - now).total_seconds()
                        send_message_to_users.apply_async(args=[message.text, user.token], countdown=delay)

                    else:
                        send_message_to_users.apply_async(args=[message.text, user.token])
            flash('Отправлено', 'success')
        except Exception as ex:
            flash(str(ex), 'error')


admin.add_view(UserAdminView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(TelegramMessageView(UserMessage, db.session, name='Message to all users'))
admin.add_view(TelegramMessage(Ticket, db.session, name='Telegram message', endpoint='telegram_message'))
admin.add_view(MyTicket(Ticket, db.session, name='My ticket', endpoint='my_ticket'))
