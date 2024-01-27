import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def lambda_handler(event, context):
    print("event:",event)
    note_id = note_content = json.loads(event['body'])['noteId']
    note_content = json.loads(event['body'])['content']

    table.put_item(
        Item={
            'NoteId': note_id,
            'Content': note_content
        }
    )

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Headers':'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps('Note created successfully')
    }
