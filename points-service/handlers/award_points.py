import json

from helpers.exceptions import DataException, RequestException
from helpers.response import Response
from models.user import User


def handler(event, context):
    try:
        body = json.loads(event['body'])

        primary_key = {}
        primary_key["user_id"] = event['pathParameters']['user_id']

        user = User.create_if_not_exist(primary_key)
        user.award_points(body)
        user.save()

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
