import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes-table')

def lambda_handler(event, context):
    note_id = json.loads(event['body'])['noteId']
    new_content = json.loads(event['body'])['content']

    response = table.update_item(
        Key={
            'NoteId': note_id
        },
        UpdateExpression='SET Content = :content',
        ExpressionAttributeValues={
            ':content': new_content
        },
        ReturnValues='UPDATED_NEW'
    )

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Headers':'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps('Note updated successfully')
    }
