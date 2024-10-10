import boto3
import json

# Initialize AWS clients for S3, Rekognition, and DynamoDB
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodbTableName = 'employee'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
employeeTable = dynamodb.Table(dynamodbTableName)
bucketName = 'fictional-vistors-images'


def lambda_handler(event, context):
    print(event)
    objectkey = event['queryStringParameters']['objectkey']
    image_bytes = s3.get_object(Bucket=bucketName, Key=objectkey)[
        'Body'].read()  # rekognition expects a binary
    response = rekognition.search_faces_by_image(
        CollectionId='employees',
        Image={'Bytes': image_bytes}
    )
    for match in response['FaceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])

        face = employeeTable.get_item(
            Key={
                'rekognitionId': match['Face'][FaceId]
            }
        )
        if 'Item' in face:
            print('Person Found: ', face['Item'])
            return buildResponse(200, {
                'message': 'Person Found',
                'firstname': face['Item']['firstname'],
                'lastname': face['Item']['lastName'],
            })
        print('person could not be regognized.')
    return buildResponse(403, {'message': 'Person Not Found'})


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response
