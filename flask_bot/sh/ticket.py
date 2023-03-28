from marshmallow import Schema, fields as f


class TicketSchema(Schema):
    id = f.Int(dump_only=True)
    title = f.Str()
    # user_id = f.Nested('UserSchema', lazy="dynamic", many=True, )
    user_id = f.Integer()
    description = f.Str()
    create_at = f.DateTime(dump_only=True)
    completed_ticket = f.DateTime()
    status = f.Boolean()

