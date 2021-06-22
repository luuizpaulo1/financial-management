from flask_restful import Resource


class DoSomething(Resource):

    @classmethod
    def get(cls):
        return "Hello world!"

    @classmethod
    def post(cls):
        pass

    @classmethod
    def put(cls):
        pass

    @classmethod
    def delete(cls):
        pass
