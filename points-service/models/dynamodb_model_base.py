from gateways.dynamodb_gateway import DynamodbGateway


class DynamodbModelBase:
    def save(self):
        DynamodbGateway.create_item(
            table_name=self.DYNAMODB_TABLE_NAME,
            payload=self.data
        )

    @classmethod
    def find(cls, primary_key):
        data = DynamodbGateway.get_item_by_primary_key(
            table_name=cls.DYNAMODB_TABLE_NAME,
            primary_key=primary_key
        )

        if data is not None:
            data["exists"] = True
            return cls(primary_key, data)
        else:
            return None