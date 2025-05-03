# Inicialización de recursos DynamoDB
import boto3, os

# Inicializar servicios de AWS
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.environ.get('FUNDS_TABLE_ARN', 'defaultARN')

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
