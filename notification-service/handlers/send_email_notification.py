import json
import os

from gateways.sns_gateway import SnsNotificationGateway
from helpers.exceptions import DataException, RequestException
from helpers.response import Response


def handler(event, context):
    try:
        body = json.loads(event['body'])
        
        print("SOMETHING IS COOL")

        primary_key = {}
        primary_key["user_id"] = event['pathParameters']['user_id']

        topic_arn = os.getenv("SNS_TOPIC_ARN")
        print(f"{topic_arn}")
        print(topic_arn.__class__)

        SnsNotificationGateway.publish_message(
            message=body["message"],
            subject="Order marked as delivered",
            topic_arn=topic_arn,
            region="ap-southeast-1"
        )

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