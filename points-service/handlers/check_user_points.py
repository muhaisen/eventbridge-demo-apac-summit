import json

from helpers.exceptions import DataException, RequestException
from helpers.response import Response
from models.user import User


def handler(event, context):
    try:
        primary_key = {}
        primary_key["user_id"] = event['pathParameters']['user_id']

        user = User.find(primary_key)

        if user is None:
            user = User.create_stub(primary_key["user_id"])

        return Response.success_json(
            {
                "data": {
                    "code": 200,
                    "message": "order_is_delivered",
                    "status": "SUCCESS",
                    "data": user.serialize()
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