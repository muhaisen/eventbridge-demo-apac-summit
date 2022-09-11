import itertools
import os

import boto3
from boto3.dynamodb.conditions import Key


class DynamodbGateway:
    @classmethod
    def create_item(cls, table_name, payload):
        client = boto3.resource('dynamodb')
        table = client.Table(table_name)

        result = table.put_item(
            Item=payload
        )

        print(result)

        return result

    @classmethod
    def scan_all(cls, table_name):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        response = table.scan()

        print("SCAN ALL")
        print(response)

        return response['Items']

    @classmethod
    def query_by_partition_key(cls, table_name, partition_key_name, partition_key_query_value):
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table(table_name)

        response = table.query(
            KeyConditionExpression=Key(partition_key_name).eq(partition_key_query_value)
        )

        return response['Items']

    @classmethod
    def get_item_by_primary_key(cls, table_name, primary_key):
        print(f"Reading from table {table_name}")
        print(f"Looking for")
        print(primary_key)

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        response = table.get_item(
            Key=primary_key
        )

        print("DB RESP")
        print(response)

        if 'Item' not in response:
            return None

        return response['Item']

    @classmethod
    def grouper(cls, iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)
        
    @classmethod
    def batch_upsert(cls, table_name, mapping_data, primary_keys):
        print(f"Inserting into table {table_name}")
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        for group in cls.grouper(mapping_data, 100):
            batch_entries = list(filter(None.__ne__, group))

            with table.batch_writer(overwrite_by_pkeys=primary_keys) as batch:
                for entry in batch_entries:
                    batch.put_item(
                        Item=entry
                    )