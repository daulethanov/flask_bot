from datetime import datetime
from . import db


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.token'))
    title = db.Column(db.String(250))
    description = db.Column(db.Text())
    create_at = db.Column(db.DateTime(), default=datetime.now())
    completed_ticket = db.Column(db.DateTime())
    status = db.Column(db.Boolean(), default=0)
    notification_time = db.Column(db.DateTime())

    def __repr__(self):
        return f'{self.user_id}'


class UserMessage(db.Model):
    __tablename__ = 'usermessage'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text())
    send_time = db.Column(db.DateTime())

    def __repr__(self):
        return self.id


