import json

from flask import Flask, make_response
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

from apps.example import Example
from config import config


class ExtendedAPI(Api):

    def init_app(self, app: Flask):
        self.app = app
        # noinspection PyTypeChecker
        self._init_app(app)

    def handle_error(self, err: Exception):
        if isinstance(err, HTTPException):
            return self.make_response(getattr(err, 'description', HTTP_STATUS_CODES.get(err.code, '')), err.code)

        return self.make_response(str(err), 500)


# db = SQLAlchemy()
cors = CORS()
api = ExtendedAPI()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db.init_app(app)
    cors.init_app(app)
    api.init_app(app)

    api.add_resource(Example, '/')

    return app


@api.representation('application/json')
def output_json(data, code, headers=None):
    if 200 <= code <= 299:
        result = {
            'success': True,
            'message': '',
            'data': data,
        }
    else:
        result = {
            'success': False,
            'message': data,
            'data': None,
        }

    response = make_response(json.dumps(result, sort_keys=True, ensure_ascii=False), 200)

    if headers:
        response.headers.extend(headers)

    return response
