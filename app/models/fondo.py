import boto3, os

# Inicializar servicios de AWS
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.environ.get('FUNDS_TABLE_ARN', 'defaultARN')

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
tabla_fondos = dynamodb.Table(DYNAMODB_TABLE)

class Fondo:
    def __init__(self, id, nombre, monto_minimo, categoria):
        self.id = id
        self.nombre = nombre
        self.monto_minimo = monto_minimo
        self.categoria = categoria

    @staticmethod
    def get_by_id(fondo_id):
        res = tabla_fondos.get_item(Key={'id': fondo_id})
        item = res.get('Item')
        if not item:
            raise Exception("Fondo no encontrado")
        return Fondo(**item)