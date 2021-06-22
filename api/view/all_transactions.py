from flask.views import View
from flask import request, render_template
from api.model.transaction import TransactionModel


class AllTransactionsView(View):
    methods = ['GET']

    def dispatch_request(self):
        if request.method == 'GET':
            transactions = TransactionModel.query.filter_by(
                is_deleted=False
            ).all()
            return render_template('all_transactions.html', transactions=transactions)
