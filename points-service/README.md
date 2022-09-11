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
```