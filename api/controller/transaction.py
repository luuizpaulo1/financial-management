from flask_restful import Resource
from flask import request
from api.model.transaction import TransactionModel
from api.model.source import SourceModel
from api.utils import missing_required_parameters


class Transaction(Resource):

    @classmethod
    def get(cls):
        """
        Retrieves transaction info.

        :return: dict
        """
        accepted_parameters = {
            'id': str
        }
        required_parameters = {
            'id': str
        }
        transaction_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, transaction_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400
        transaction = TransactionModel.find_transaction_by_id(transaction_data['id'])
        if transaction:
            return transaction.json()
        else:
            return {'msg': 'transaction not found'}, 404

    @classmethod
    def post(cls):
        """
        Creates transaction.

        :return: dict
        """
        accepted_parameters = {
            'user_id': str,
            'source_id': str,
            'category': str,
            'subcategory': str,
            'description': str,
            'amount': int,
            'installments': int
        }
        required_parameters = {
            'user_id': str,
            'source_id': str,
            'amount': int,
        }
        transaction_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, transaction_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        source = SourceModel.find_source_by_id(transaction_data['source_id'])
        if not source:
            return {'msg': 'source_id not found'}, 404
        if source.type == 'debit_card' and transaction_data.get('installments'):
            return {'msg': 'debit_card transactions do not have installments attribute'}, 400
        elif source.type == 'credit_card' and not transaction_data.get('installments'):
            transaction_data['installments'] = 1
        transaction_data['source'] = source

        transaction = TransactionModel(**transaction_data)
        transaction.save_transaction()
        return transaction.json(), 201

    @classmethod
    def put(cls):
        """
        Updates transaction.

        :return: dict
        """
        accepted_parameters = {
            'id': str,
            'source_id': str,
            'category': str,
            'subcategory': str,
            'description': str,
            'amount': int,
            'installments': int
        }
        required_parameters = {
            'id': str
        }
        transaction_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, transaction_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}

        transaction = TransactionModel.find_transaction_by_id(transaction_data['id'])
        if transaction:
            update_args = {key: value for key, value in transaction_data.items() if key in transaction.update_args}
            transaction.update_transaction(**update_args)
            return transaction.json()
        else:
            return {'msg': 'user not found'}, 404

    @classmethod
    def delete(cls):
        """
        Deletes transaction.

        :return: dict
        """
        accepted_parameters = {
            'id': str
        }
        required_parameters = {
            'id': str
        }
        transaction_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, transaction_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        transaction = TransactionModel.find_transaction_by_id(transaction_data['id'])
        if transaction:
            transaction.delete_transaction()
            return {'msg': 'transaction deleted'}, 200
        else:
            return {'msg': 'transaction not found'}, 404
