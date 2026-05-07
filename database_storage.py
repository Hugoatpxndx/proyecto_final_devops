import boto3
import time
from botocore.exceptions import ClientError

# Configuraciones iniciales
REGION = 'us-east-1'
sts_client = boto3.client('sts', region_name=REGION)
account_id = sts_client.get_caller_identity()['Account']

# Clientes de Boto3
s3_client = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)

BUCKET_NAME = f'devops-almacenamiento-seguro-{account_id}'
TABLE_NAME = 'TablaOperacionesDevOps'

def configurar_s3():
    print(f"\n--- Iniciando Configuración de S3 ---")
    try:
        # 1. Crear el bucket
        print(f"Creando bucket S3: {BUCKET_NAME}...")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        
        # 2. Implementar políticas de versión
        print("Habilitando versionamiento de objetos...")
        s3_client.put_bucket_versioning(
            Bucket=BUCKET_NAME,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        # 3. Habilitar cifrado de datos en reposo (AES256)
        print("Habilitando cifrado de datos en reposo...")
        s3_client.put_bucket_encryption(
            Bucket=BUCKET_NAME,
            ServerSideEncryptionConfiguration={
                'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
            }
        )
        
        # 4. Implementar reglas de ciclo de vida (Borrar en 30 días)
        print("Aplicando reglas de ciclo de vida (eliminación a los 30 días)...")
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=BUCKET_NAME,
            LifecycleConfiguration={
                'Rules': [{
                    'ID': 'BorradoAutomaticoLogs',
                    'Filter': {'Prefix': ''},
                    'Status': 'Enabled',
                    'Expiration': {'Days': 30}
                }]
            }
        )
        
        # 5. Automatizar la carga de archivos
        print("Subiendo archivo 'log_prueba.txt' a S3...")
        s3_client.upload_file('log_prueba.txt', BUCKET_NAME, 'logs/log_prueba.txt')
        print("¡Archivo subido exitosamente!")
        
    except ClientError as e:
        print(f"Error en S3: {e}")

def operaciones_dynamodb():
    print(f"\n--- Iniciando Operaciones en DynamoDB ---")
    try:
        # 1. Crear tabla con clave primaria
        print(f"Creando tabla {TABLE_NAME} (esto tomará unos segundos)...")
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'ID_Registro', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'ID_Registro', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
        print("¡Tabla creada y activa!")

        # 2. Insertar un registro
        print("Insertando registro en DynamoDB...")
        table.put_item(
            Item={
                'ID_Registro': '001',
                'Servicio': 'AppWeb',
                'Estado': 'Desplegado'
            }
        )

        # 3. Modificar el registro
        print("Modificando registro existente...")
        table.update_item(
            Key={'ID_Registro': '001'},
            UpdateExpression='SET Estado = :val1',
            ExpressionAttributeValues={':val1': 'Actualizado y Monitoreado'}
        )

        # 4. Eliminar el registro
        print("Eliminando registro de DynamoDB...")
        table.delete_item(Key={'ID_Registro': '001'})
        print("¡Ciclo CRUD en DynamoDB completado con éxito!")

    except ClientError as e:
        print(f"Error en DynamoDB: {e}")

if __name__ == '__main__':
    configurar_s3()
    operaciones_dynamodb()
    print("\n--- ¡Todas las operaciones de Bases de Datos y Almacenamiento finalizaron correctamente! ---\n")
