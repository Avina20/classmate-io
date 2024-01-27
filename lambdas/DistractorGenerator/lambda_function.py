import boto3
import json
import requests

def lambda_handler(event, context):
    print("event",event)
    body = json.loads(event['body'])
    content = body['content']
    print("content", content)
    
    modified_content = '|'.join(content.split('.'))
    print("modified content", modified_content)
    
        
    flask_app_url = 'http://3.89.27.97'
    flask_app_url_with_param = f'{flask_app_url}?summary={modified_content}'

    try:
        response = requests.get(flask_app_url_with_param)
        print('response',response.text)
        return {
            'statusCode': response.status_code,
            'headers':{
                'Access-Control-Allow-Headers':'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': response.text
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers':{
                'Access-Control-Allow-Headers':'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': str(e)
        }
