import boto3, os
import uuid
from datetime import datetime

# Inicializar servicios de AWS
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.environ.get('TRANSACTIONS_TABLE_ARN', 'defaultARN')

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
tabla_transacciones = dynamodb.Table(DYNAMODB_TABLE)

class Transaccion:
    @staticmethod
    def create(tipo, fondo_id, usuario_id, monto):
        transaccion = {
            'id': str(uuid.uuid4()),
            'tipo': tipo,
            'fondo_id': fondo_id,
            'usuario_id': usuario_id,
            'monto': monto,
            'timestamp': str(datetime.datetime.now().timestamp())
        }
        tabla_transacciones.put_item(Item=transaccion)

    @staticmethod
    def get_by_usuario(usuario_id):
        res = tabla_transacciones.scan()
        return [item for item in res['Items'] if item['usuario_id'] == usuario_id]