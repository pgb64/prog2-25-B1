from flask import Response
import json

class ApiResponse:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404

    @staticmethod
    def response(state, message, data, code):
        if data is None:
            response = {
                'status': state,
                'message': message,
            }
        else:
            response = {
                'status': state,
                'message': message,
                'data': data
            }
        return Response(json.dumps(response, indent=2), status=code, mimetype='application/json')

    @staticmethod
    def success(message, data):
        return ApiResponse.response('success', message, data, code=ApiResponse.OK)

    @staticmethod
    def error(message, code=None):
        if code is None:
            code = ApiResponse.BAD_REQUEST
        return ApiResponse.response('error', message, None, code)

    @staticmethod
    def not_found(message):
        return ApiResponse.error(message, ApiResponse.NOT_FOUND)

    @staticmethod
    def bad_request(message):
        return ApiResponse.error(message, ApiResponse.BAD_REQUEST)

    @staticmethod
    def unauthorized(message):
        return ApiResponse.error(message, ApiResponse.UNAUTHORIZED)


