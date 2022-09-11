# Order Service

## Developing

```sh
serverless offline --region ap-southeast-1 --stage dev
```

## Initial Project Setup

```sh
python3 -m venv venv
source venv/bin/activate

pip install boto3
pip install pytz


pip freeze > requirements.txt

serverless deploy --region ap-southeast-1 --stage dev
serverless plugin install -n serverless-offline
serverless plugin install -n serverless-python-requirements 

```



Create Order

```json

POST - /orders

{
  "user_id": "U101",
  "amount": 1000,
  "items": [
    {"name": "Fresh Milk", "price": 1.5},
    {"name": "Golden Liquior", "price": 3.0}
  ]
}
```

Mark order as delivered

```json

POST - users/{user_id}/orders/{orders_id}/deliver

{
  "delivered_at": "Sep 17, 2022 1:00PM GMT+7"
}
```