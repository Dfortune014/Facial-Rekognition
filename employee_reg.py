import boto3

# Initialize AWS clients for S3, Rekognition, and DynamoDB
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodbTableName = 'employee'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
employeeTable = dynamodb.Table(dynamodbTableName)

# Lambda function handler


def lambda_handler(event, context):
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']  # Get S3 bucket name
    # Get S3 object key (image file name)
    key = event['Records'][0]['s3']['object']['key']

    try:
        # Call the function to index the employee image using Rekognition
        response = index_employee_image(bucket, key)
        print(response)

        # If the Rekognition API call is successful, extract and store Face ID
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # Extract the FaceId from the response
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            name = key.split('.')[0].split('_')
            firstName = name[0]
            lastname = name[1]
            register_employee(faceId, firstName, lastname)
        return response

    except Exception as e:
        print(e)
        print('Error processing employee image {} from bucket{}.'.format(key, bucket))
        raise e

# Helper function to index the employee image using Rekognition


def index_employee_image(bucket, key):
    response = rekognition.index_faces(
        CollectionId='employee',  # Name of the Rekognition collection
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        # Use the image file name (without extension) as the external ID
        ExternalImageId=key.split(".")[0],
        MaxFaces=1,  # Only detect one face
        QualityFilter="AUTO",
        DetectionAttributes=['ALL']
    )
    return response


def register_employee(faceId, firstName, lastname):
    employeeTable.put_item(
        Item={
            'rekognitionId': faceId,
            'firstName': firstName,
            'lastName': lastname
        }
    )
