from flask_restful import Resource
from flask import request
from api.model.source import SourceModel
from api.utils import missing_required_parameters


class Source(Resource):

    @classmethod
    def get(cls):
        """
        Retrieves source info.

        :return: dict
        """
        accepted_parameters = {
            'id': str
        }
        required_parameters = {
            'id': str
        }
        source_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, source_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        source = SourceModel.find_source_by_id(source_data['id'])
        if source:
            return source.json()
        else:
            return {'msg': 'source not found'}, 404

    @classmethod
    def post(cls):
        """
        Creates source.

        :return: dict
        """
        accepted_parameters = {
            'user_id': str,
            'type': str,
            'name': str,
            'balance': int,
            'closing_day': int,
            'limit': int
        }
        required_parameters = {
            'user_id': str,
            'type': str,
            'name': str,
            'balance': int
        }
        source_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        if source_data['type'] not in ['credit_card', 'debit_card']:
            return {'msg': 'type must be either credit_card or debit_card'}, 400

        if source_data['type'] == 'debit_card':
            if source_data.get('closing_date') or source_data.get('limit'):
                return {'msg': 'debit_card do not have closing_day or limit attributes'}, 400

        if source_data['type'] == 'credit_card':
            if not source_data.get('closing_date') or not source_data.get('limit'):
                return {'msg': 'credit_card must have closing_day and limit attributes'}, 400

        missing_parameters = missing_required_parameters(required_parameters, source_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}

        source = SourceModel(**source_data)
        source.save_source()
        return source.json(), 201

    @classmethod
    def put(cls):
        """
        Updates source.

        :return: dict
        """
        accepted_parameters = {
            'id': str,
            'name': str,
            'balance': str,
            'closing_date': int,
            'limit': int
        }
        required_parameters = {
            'id': str
        }
        source_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, source_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}

        source = SourceModel.find_source_by_id(source_data['id'])
        if source:
            if source.type == 'debit_card':
                if source_data.get('closing_date') or source_data.get('limit'):
                    return {'msg': 'debit_card do not have closing_day or limit attributes'}, 400
            update_args = {key: value for key, value in source_data if SourceModel.update_args}
            source.update_source(**update_args)
            return source.json()
        else:
            return {'msg': 'user not found'}, 404

    @classmethod
    def delete(cls):
        """
        Deletes source.

        :return: dict
        """
        accepted_parameters = {
            'id': str
        }
        required_parameters = {
            'id': str
        }
        source_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, source_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        source = SourceModel.find_source_by_id(source_data['id'])
        if source:
            source.delete_source()
            return {'msg': 'source deleted'}, 200
        else:
            return {'msg': 'source not found'}, 404
