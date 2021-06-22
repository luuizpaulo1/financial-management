from flask.views import View
from flask import request, render_template
from api.model.user import UserModel


class UserView(View):
    methods = ['GET']

    def dispatch_request(self, id):
        if request.method == 'GET':
            user = UserModel.find_user_by_id(id)
            return render_template('user.html', user=user)
