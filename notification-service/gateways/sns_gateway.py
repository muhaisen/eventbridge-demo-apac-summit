import json
import os
from decimal import Decimal

import boto3


class SnsNotificationGateway():
    @classmethod
    def publish_message(cls, message, subject, topic_arn, region):
        client = boto3.client('sns', region)

        print("SENDING SNS MESSAGE TO")
        print(topic_arn)
        print("message")
        print(message)
        print("========")

        response = client.publish(
            TopicArn = topic_arn,   
            Subject = subject,
            Message = message
        )

        return response
