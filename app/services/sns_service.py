import boto3, os

# Inicializar servicios de AWS
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SNS_URL = os.environ.get('CLIENT_SNS_URL', 'defaultARN')

##dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

class SNSService:
    @staticmethod
    def enviar_notificacion(usuario, metodo, mensaje):
        sns = boto3.client('sns', region_name=AWS_REGION)

# SNS_URL arn:aws:sns:us-east-1:123456789012:EmailTopic
        if metodo == "email":
            sns.publish(TopicArn=SNS_URL, Message=mensaje)
        elif metodo == "sms":
            sns.publish(PhoneNumber=usuario.telefono, Message=mensaje)


