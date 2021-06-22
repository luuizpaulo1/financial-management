from flask_restful import Resource
from flask import request
from datetime import datetime
from api.model.user import UserModel
from api.utils import missing_required_parameters


class User(Resource):

    @classmethod
    def get(cls):
        """
        Retrieves user info.

        :return: dict
        """
        accepted_parameters = {'id': str}
        required_parameters = {'id': str}
        user_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, user_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        user = UserModel.find_user_by_id(user_data['id'])
        if user:
            return user.json()
        else:
            return {'msg': 'user not found'}, 404

    @classmethod
    def post(cls):
        """
        Creates user.

        :return: dict
        """
        accepted_parameters = {
            'name': str,
            'document': str,
            'birth_date': str
        }
        required_parameters = {
            'name': str,
            'document': str,
            'birth_date': str
        }
        user_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, user_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        try:
            user_data['birth_date'] = datetime.strptime(user_data.get('birth_date'), "%Y-%m-%d")
        except ValueError:
            return {'msg': '"birth_date" value does not match "YYYY-MM-DD" date format'}

        user = UserModel(**user_data)
        user.save_user()
        return user.json(), 201

    @classmethod
    def put(cls):
        """
        Updates user.

        :return: dict
        """
        accepted_parameters = {
            'id': str,
            'name': str,
            'document': str,
            'birth_date': str
        }
        required_parameters = {
            'id': str
        }
        user_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, user_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        try:
            user_data['birth_date'] = datetime.strptime(user_data.get('birth_date'), "%Y-%m-%d")
        except ValueError:
            return {'msg': '"birth_date" value does not match "YYYY-MM-DD" date format'}

        user = UserModel.find_user_by_id(user_data['id'])
        if user:
            update_args = {key: value for key, value in user_data.items() if key in UserModel.update_args}
            user.update_user(**update_args)
            return user.json()
        else:
            return {'msg': 'user not found'}, 404

    @classmethod
    def delete(cls):
        """
        Deletes user.

        :return: dict
        """
        accepted_parameters = {
            'id': str
        }
        required_parameters = {
            'id': str
        }
        user_data = {key: value for key, value in request.json.items() if key in accepted_parameters}

        missing_parameters = missing_required_parameters(required_parameters, user_data)
        if missing_parameters:
            return {'msg': f'missing required parameter(s): {", ".join(missing_parameters)}'}, 400

        user = UserModel.find_user_by_id(user_data['id'])
        if user:
            user.delete_user()
            return {'msg': 'user deleted'}, 200
        else:
            return {'msg': 'user not found'}, 404
