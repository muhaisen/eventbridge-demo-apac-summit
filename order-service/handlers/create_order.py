import json

from helpers.exceptions import RequestException
from helpers.response import Response
from models.order import Order


def handler(event, context):
    try:
        body = json.loads(event['body'])
        order = Order.create(body)
        
        order.save()
        
        print("Creating an order!!! <3 <3")

        return Response.success_json(
            {
                "data": {
                    "code": 200,
                    "message": "order_is_created",
                    "status": "SUCCESS",
                    "data": order.serialize()
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
