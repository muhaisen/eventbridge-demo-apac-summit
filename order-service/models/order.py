import os
import random
import string

from helpers.exceptions import DataException, RequestException
from models.dynamodb_model_base import DynamodbModelBase


class Order(DynamodbModelBase):
    DYNAMODB_TABLE_NAME = os.getenv("ORDERS_TABLE")

    def __init__(self, primary_key, data):
        self.primary_key = primary_key
        self.data = data

    def mark_as_delivered(self):
        if self.data["status"] == "confirmed":
            self.data["status"] = "delivered"
        else:
            raise DataException("Only confirmed orders can be marked as delivered")
    
    def serialize(self):
        return {
            "order_number": self.data["order_number"],
            "user_id": self.data["user_id"],
            "status": self.data["status"]
        }

    @classmethod
    def generate_code(cls, prefix, string_length):
        letters = string.ascii_uppercase
        return prefix + ''.join(random.choice(letters) for i in range(string_length))
    
    @classmethod
    def extract_primary_key(cls, data):
        try:
            return {
                "user_id": data["user_id"],
                "order_number": cls.generate_code("R", 10)
            }
        except Exception as e:
            raise RequestException("The primary key cannot be formed")

    @classmethod
    def create(cls, data):
        primary_key = Order.extract_primary_key(data)
        order = Order.find(primary_key)

        if order is not None:
            raise RequestException("The order_id already exists for this user")
        
        data = {**data, **primary_key}
        data["status"] = "confirmed"
        return cls(primary_key, data)