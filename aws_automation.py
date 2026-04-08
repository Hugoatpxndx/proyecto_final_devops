import boto3
import sys
from botocore.exceptions import ClientError

REGION = 'us-east-1'
AMI_ID = 'ami-0a3c3a20c09d6f377' 
INSTANCE_TYPE = 't2.micro'
MAX_LAB_INSTANCES = 9

ec2_client = boto3.client('ec2', region_name=REGION)
ec2_resource = boto3.resource('ec2', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)

def obtener_conteo_instancias():
    response = ec2_client.describe_instances()
    count = 0
    for reservation in response['Reservations']:
        count += len(reservation['Instances'])
    return count

def aprovisionar_ec2(cantidad):
    actuales = obtener_conteo_instancias()
    disponibles = MAX_LAB_INSTANCES - actuales
    
    print(f"\n[EC2] Instancias actuales: {actuales} | Limite: {MAX_LAB_INSTANCES}")
    
    if cantidad > disponibles:
        print(f"Error: No puedes crear {cantidad} instancias. Solo quedan {disponibles} espacios.")
        return
    
    try:
        print(f"Aprovisionando {cantidad} instancias...")
        instancias = ec2_resource.create_instances(
            ImageId=AMI_ID,
            MinCount=cantidad,
            MaxCount=cantidad,
            InstanceType=INSTANCE_TYPE,
            IamInstanceProfile={'Name': 'LabInstanceProfile'},
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Project', 'Value': 'ProyectoFinalDevOps'}]
            }]
        )
        for i in instancias:
            print(f"Instancia creada: {i.id}")
    except ClientError as e:
        print(f"Error de AWS: {e}")

def listar_s3_completo():
    print("\n[S3] Listando buckets y objetos...")
    try:
        buckets = s3_client.list_buckets()['Buckets']
        if not buckets:
            print("No hay buckets disponibles.")
            return

        for bucket in buckets:
            name = bucket['Name']
            print(f"\nBucket: {name}")
            objs = s3_client.list_objects_v2(Bucket=name)
            if 'Contents' in objs:
                for obj in objs['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("  (Bucket vacio)")
    except ClientError as e:
        print(f"Error al acceder a S3: {e}")

def generar_reporte():
    print("\n" + "="*40)
    print("REPORTE AUTOMATICO DE RECURSOS AWS")
    print("="*40)
    
    instancias = ec2_client.describe_instances()
    estados = {}
    for res in instancias['Reservations']:
        for ins in res['Instances']:
            status = ins['State']['Name']
            estados[status] = estados.get(status, 0) + 1
    
    print("Estado de Instancias EC2:")
    if not estados: print("  Ninguna instancia encontrada.")
    for state, count in estados.items():
        print(f"  - {state.capitalize()}: {count}")
    
    bucket_count = len(s3_client.list_buckets()['Buckets'])
    print(f"\nTotal de Buckets S3: {bucket_count}")
    print("="*40 + "\n")

if __name__ == "__main__":
    generar_reporte()
    listar_s3_completo()
    # aprovisionar_ec2(1)
