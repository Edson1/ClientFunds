import boto3, os

# Inicializar servicios de AWS
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMODB_TABLE = os.environ.get('USERS_TABLE_ARN', 'defaultARN')

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
tabla_usuarios = dynamodb.Table(DYNAMODB_TABLE) #'Usuarios')

class Usuario:
    def __init__(self, id, nombre, saldo, fondos=[]):
        self.id = id
        self.nombre = nombre
        self.saldo = saldo
        self.fondos = fondos

    def save(self):
        tabla_usuarios.put_item(Item=self.__dict__)

    @staticmethod
    def get_by_id(usuario_id):
        res = tabla_usuarios.get_item(Key={'id': usuario_id})
        item = res.get('Item')
        if not item:
            raise Exception("Usuario no encontrado")
        return Usuario(**item)