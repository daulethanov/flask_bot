from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        for role in current_user.roles:
            if role.name == 'admin':
                return True
        return False


class MyModelViewTicket(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        for role in current_user.roles:
            if role.name == 'developer':
                return True
        return False
