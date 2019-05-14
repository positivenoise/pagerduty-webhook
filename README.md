# PagerDuty Webhook

Flask + Serverless + Lambda webhook for custom action responses sent from PagerDuty
___
## Requirements

- Python3
- Pipenv
- Serverless

Setup pipenv with `pipenv --three`

Install requirements with:
```
pipenv install flask boto3 requests pypd
```

Install serverless plugins with
```
pipenv run serverless plugin install -n serverless-wsgi
pipenv run serverless plugin install -n serverless-python-requirements
```
Test locally with `pipenv run serverless wsgi serve`
___
## Deployment

Ensure you have your AWS credentials setup in serverless
```
serverless config credentials --provider aws --key <KEY> --secret <SECRET>
```
deploy with `pipenv run serverless deploy`, undeploy with `pipenv run serverless remove`

curl command to test with:
``` 
curl.exe -H "Content-Type: application/json" -X POST http://localhost/terminate -d "@custom_action.json"
``` 

___
## Resources
- Custom incident actions in PD:
https://support.pagerduty.com/docs/custom-incident-actions
- Webhooks overview: https://v2.developer.pagerduty.com/docs/webhooks-v2-overview