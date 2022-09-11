import os
import random
import string
from decimal import Decimal

from helpers.exceptions import DataException, RequestException
from models.dynamodb_model_base import DynamodbModelBase


class User(DynamodbModelBase):
    DYNAMODB_TABLE_NAME = os.getenv("USERS_TABLE")

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
            "points": self.data["points"],
            "user_id": self.data["user_id"],
            "exists": self.data["exists"]
        }
    
    def award_points(self, body):
        points_for_order_raw = str(round((body["total"] / 10), 4))
        points_for_order = Decimal(points_for_order_raw)
        
        print(points_for_order_raw)
        print(points_for_order)

        self.data["orders"].append({
            "order_id": body["order_id"],
            "points": points_for_order
        })

        self.data["points"] += points_for_order

    @classmethod
    def create_stub(cls, user_id):
        return User({"user_id": user_id}, {"user_id": user_id, "points": 0, "exists": False})

    @classmethod
    def generate_code(cls, prefix, string_length):
        letters = string.ascii_uppercase
        return prefix + ''.join(random.choice(letters) for i in range(string_length))
    
    @classmethod
    def extract_primary_key(cls, data):
        try:
            return {
                "user_id": data["user_id"]
            }
        except Exception as e:
            raise RequestException("The primary key cannot be formed")

    @classmethod
    def create_if_not_exist(cls, data):
        primary_key = User.extract_primary_key(data)
        user = User.find(primary_key)

        if user is not None:
            return user

        user_data = {
            "points": Decimal(0),
            "orders": [],
            "exists": True
        }
        
        data = {**user_data, **primary_key}

        return cls(primary_key, data)