import json
import os

from gateways.eventbridge_gateway import EventbridgeGateway
from helpers.response import Response


class EventbridgeEvent:
    EVENT_BUS = os.environ.get("EVENT_BUS_NAME")
    SOURCE_URL = os.environ.get("EVENT_SOURCE_NAME")

    def __init__(self, event_name, event_body):
        self.event_name = event_name
        self.event_body = event_body

    def serialize(self):
        json_details = Response.construct_json_body(self.event_body)

        return {
            "Source": self.SOURCE_URL,
            "DetailType": self.event_name,
            "Detail": json_details,
            "EventBusName": self.EVENT_BUS,
        }

    def send(self):
        event_json = self.serialize()
        EventbridgeGateway.put_event(event_json)