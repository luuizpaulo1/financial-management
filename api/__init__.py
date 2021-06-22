from flask import Blueprint
from flask_restful import Api
from api.controller import DoSomething
from api.controller.user import User
from api.controller.transaction import Transaction
from api.controller.source import Source
from api.view.do_something import DoSomethingView
from api.view.all_users import AllUsersView
from api.view.all_transactions import AllTransactionsView
from api.view.all_sources import AllSourcesView
from api.view.user import UserView
from api.view.user_sources import UserSourcesView
from api.view.user_transactions import UserTransactionsView


def setup_blueprint(app):
    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api = Api(blueprint)

    api.add_resource(DoSomething, '/')
    api.add_resource(User, '/users')
    api.add_resource(Transaction, '/transactions')
    api.add_resource(Source, '/sources')

    app.add_url_rule("/", view_func=DoSomethingView.as_view('do_something'))
    app.add_url_rule("/users/", view_func=AllUsersView.as_view('all_users_view'))
    app.add_url_rule("/transactions/", view_func=AllTransactionsView.as_view('all_transactions_view'))
    app.add_url_rule("/sources/", view_func=AllSourcesView.as_view('all_sources_view'))

    app.add_url_rule("/users/<id>/", view_func=UserView.as_view('user_view'))
    app.add_url_rule("/users/<user_id>/transactions", view_func=UserTransactionsView.as_view('user_transactions_view'))
    app.add_url_rule("/users/<user_id>/sources", view_func=UserSourcesView.as_view('user_sources_view'))

    return blueprint
