from marshmallow import Schema, fields as f
from .ticket import TicketSchema


class RoleSchema(Schema):
    id = f.Int(dump_only=True)
    name = f.Str()
    description = f.Str()


class UserSchema(Schema):
    id = f.Integer()
    username = f.Str()
    email = f.Email(required=True)
    password = f.Str()
    token = f.Int()
    active = f.Bool()
    create_at = f.DateTime(dump_only=True)
    reminder = f.DateTime()
    ticket = f.Nested(TicketSchema)
    roles = f.Nested(RoleSchema(only=('name',), many=True))
    notification_time = f.DateTime()
