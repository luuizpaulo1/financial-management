from flask.views import View
from flask import request, render_template
from api.model.user import UserModel


class AllUsersView(View):
    methods = ['GET']

    def dispatch_request(self):
        if request.method == 'GET':
            users = UserModel.query.filter_by(
                is_deleted=False
            ).all()
            return render_template('all_users.html', users=users)
