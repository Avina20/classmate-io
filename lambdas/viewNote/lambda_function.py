import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def lambda_handler(event, context):
    response = table.scan()

    notes = response.get('Items', [])

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Headers':'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(notes)
    }
