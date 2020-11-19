from flask_restful import Resource, reqparse, fields, marshal_with


class ValidationError(Exception):
    pass


class User:

    def __init__(self, _id, name, age):
        self._id = _id
        self.name = name
        self.age = age


user_fields = {
    'id': fields.Integer(attribute='_id'),
    'name': fields.String(default='Unknown'),
    'age': fields.Integer(default=20),
}


class Example(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('id', type=int, location=['args', 'form'], help='Rate cannot be converted', required=True)
    _parser.add_argument('name', location=['args', 'form'])
    _parser.add_argument('age', type=int, location=['args', 'form'])

    def get(self):
        args = self._parser.parse_args()
        return {
            'id': args.id,
            'name': args.name,
        }

    @marshal_with(user_fields, envelope='users')
    def post(self):
        args = self._parser.parse_args()
        return [User(args.id, args.name, args.name)]

    def put(self):
        raise ValidationError('failed')
