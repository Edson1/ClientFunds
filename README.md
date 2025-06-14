# Microservicio de fondos del cliente

## Cómo crear IaaC del proyecto en cloud AWS desde CloudFormation:
Importar en CloudFormation el serverless.yml , que crea una AWS ECS cluster en modo fargate (sin servidor EC2 explicito), que almacena en DynamoDB (base de datos NoSQL), y envia notificaciones SNS. Ver diagrama de arquitectura Amazon Web Services (AWS) adjunto en este repositorio.

El Codigo python se compiló en una imagen de docker subida a un repositorio ECR publico que permite su descarga posterior en nuestra arquitectura AWS:
Image: "public.ecr.aws/e8s6v1o2/mypublicimages/clientapp:latest"

## Decisiones técnicas:
La API esta configurada para accesos desde cualquier origen (CORS) para facilitar las pruebas iniciales, igualmente tampoco requiere API keys o algun otro tipo de autorizacion como tokens que obviamente se requieren para mantener la seguridad del microservicio.

## Pueden probar el microservicio usando el endpoint con acceso publico. 
aws url...

# APIs Propuestas 
Método	Ruta	Descripción
POST	/suscripciones	Suscribirse a un fondo
POST	/cancelaciones	Desvincularse de un fondo
GET	/transacciones	Ver historial de transacciones

Ejemplo: Suscribirse a un fondo
    Valida si ya está suscrito.
    Verifica monto mínimo y saldo.
    Actualiza saldo.
    Crea transacción.
    Envía notificación SNS.

# Instalar dependencias del proyecto en python:
pip install -r requirements.txt

1. run local sin docker, puerto es 8000 directamente
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug  
ó
2. build image solamente pero con network fijada manualmente al run en container>
docker build -t appimage . 

## Poblar tablas con datos de inicializacion dados en el PDF de la prueba
1 FPV_EL CLIENTE_RECAUDADORA COP $75.000 FPV
2 FPV_EL CLIENTE_ECOPETROL COP $125.000 FPV
3 DEUDAPRIVADA COP $50.000 FIC
4 FDO-ACCIONES COP $250.000 FIC
5 FPV_EL CLIENTE_DINAMICA COP $100.000 FPV

# Herramientas usadas
Framework: FastAPI (por ser liviano, rápido y amigable con OpenAPI/Swagger)
Base de datos: DynamoDB (NoSQL de AWS)
Mensajería: AWS SNS (para notificaciones por email/SMS)

# Estructura del Proyecto
fondos_api/
│
├── app/
│   ├── controllers/
│   │   └── fondo_controller.py
│   ├── models/
│   │   ├── fondo.py
│   │   ├── usuario.py
│   │   └── transaccion.py
│   ├── services/
│   │   ├── dynamodb_service.py
│   │   ├── sns_service.py
│   │   └── validator.py
│   └── routes/
│       └── api.py
│
├── main.py
├── requirements.txt
└── config.py

# Modelo de Datos Simplificado
Usuarios: id, nombre, saldo
Fondos: id, nombre, monto_minimo, categoria
Transacciones: id, usuario_id, fondo_id, tipo, monto, timestamp

Usuario
{
  "usuario_id": "123",
  "nombre": "Cliente",
  "saldo": 500000,
  "fondos_activos": [
    {
      "fondo_id": 1,
      "monto_suscrito": 100000
    }
  ]
}

Fondo
{
  "fondo_id": 1,
  "nombre": "Fondo A",
  "monto_minimo": 100000,
  "categoria": "FIC"
}

Transacción
{
  "transaccion_id": "uuid",
  "usuario_id": "123",
  "fondo_id": 1,
  "tipo": "apertura" | "cancelacion",
  "monto": 100000,
  "timestamp": "2025-04-30T12:00:00"
}

## Ejecutar pruebas unitarias de la funcion lambda con:
pip install boto3 moto

python -m unittest test.py

# Update image en ECR con password y token de autenticacion de AWS 
docker push public.ecr.aws/e8s6v1o2/mypublicimages/clientapp:latest





