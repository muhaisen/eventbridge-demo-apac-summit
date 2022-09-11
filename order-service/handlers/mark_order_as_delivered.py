import json

from helpers.exceptions import DataException, RequestException
from helpers.response import Response
from models.order import Order


def handler(event, context):
    try:
        body = json.loads(event['body'])

        primary_key = {}
        primary_key["user_id"] = event['pathParameters']['user_id']
        primary_key["order_number"] = event['pathParameters']['order_number']

        order = Order.find(primary_key)
        order.mark_as_delivered()
        order.save()

        return Response.success_json(
            {
                "data": {
                    "code": 200,
                    "message": "order_is_delivered",
                    "status": "SUCCESS",
                    "data": {}
                }
            },
            200
        )
    except RequestException as e:
        return Response.failed_json(
            {
                "error": {
                    "code": 400,
                    "message": {
                        "error": str(e),
                    },
                    "status": "INVALID_REQUEST",
                }
            }
        )

    except DataException as e:
        return Response.failed_json(
            {
                "error": {
                    "code": 400,
                    "message": {
                        "error": str(e),
                    },
                    "status": "INVALID_DATA",
                }
            }
        )