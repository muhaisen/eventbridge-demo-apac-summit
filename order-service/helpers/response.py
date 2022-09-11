import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

class Response:
    @staticmethod
    def construct_json_body(body, default = None):
        return json.dumps(body, default=default, cls=DecimalEncoder)

    @staticmethod
    def success_json(body, code = 200, headers = {}, default = None):
        response = {
            'statusCode': code,
            'body': Response.construct_json_body(body, default),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            }
        }

        if bool(headers):
            response['headers'] = headers

        return response
    
    @staticmethod
    def failed_json(body, code = 422, headers = {}, default = None):
        response = {
            'statusCode': code,
            'body': json.dumps(body, default=default),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            }
        }

        if bool(headers):
            response['headers'] = headers

        return response