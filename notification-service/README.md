## Developing

```sh

ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

serverless offline --region ap-southeast-1 --stage dev --accountId $ACCOUNT_ID
serverless deploy --region ap-southeast-1 --stage dev --accountId $ACCOUNT_ID
```


## Initial Project Setup

```sh
deactivate
python3 -m venv venv
source venv/bin/activate

pip install boto3
pip install pytz


pip freeze > requirements.txt




serverless plugin install -n serverless-offline
```