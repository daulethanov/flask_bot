from datetime import datetime
import pytz
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from ..model import db
from ..model.ticket import Ticket
from ..model.user import User
from ..sh.ticket import TicketSchema
from ..sh.user import UserSchema


ticket = Blueprint('tickets', __name__, url_prefix='/api/ticket')

ticket_schema = TicketSchema(many=True)


@ticket.route('/list', methods=['GET'])
def ticket_list():
    tickets = Ticket.query.all()
    ticket_mp = TicketSchema().dump(tickets)
    return jsonify({
        'result': ticket_mp
    })


@ticket.route('/create', methods=['POST'])
def ticket_create():
    ticket_schemas = TicketSchema()
    try:
        ticket_data = ticket_schemas.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    create_ticket = Ticket(
        title=ticket_data['title'],
        user_id=ticket_data['user_id'],
        description=ticket_data['description'],
    )
    db.session.add(create_ticket)
    db.session.commit()
    ticket_schemas.dump(create_ticket)


@ticket.route('/send_date', methods=['PUT', "POST"])
def send_message():
    users = User.query.filter(User.notification_time != None).all()
    local_kz = pytz.timezone('Asia/Almaty')
    current_time = datetime.now(local_kz)
    try:
        user_data = UserSchema(only=['id', 'notification_time']).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user_create = User(
        id=user_data['id'],
        notification_time=user_data['notification_time']
    )
    db.session.add(user_create)
    db.session.commit()
    while True:
        for user in users:
            if current_time == user_data['notification_time']:
                message = "Время оповещения наступило!"
                user.notification_time = None
                db.session.commit()




