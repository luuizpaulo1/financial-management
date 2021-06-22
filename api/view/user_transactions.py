from flask.views import View
from flask import request, render_template
from api.model.user import UserModel


class UserTransactionsView(View):
    methods = ['GET']

    def dispatch_request(self, user_id):
        if request.method == 'GET':
            user = UserModel.find_user_by_id(user_id)
            return render_template('user_transactions.html', transactions=user.transactions)
