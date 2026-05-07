import boto3

REGION = 'us-east-1'
ec2_client = boto3.client('ec2', region_name=REGION)
ssm_client = boto3.client('ssm', region_name=REGION)

def obtener_instancia():
    # Busca la instancia que creamos con CloudFormation
    respuesta = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['Servidor-App-SSM']}])
    for reserva in respuesta['Reservations']:
        for instancia in reserva['Instances']:
            if instancia['State']['Name'] == 'running':
                return instancia['InstanceId']
    return None

def desplegar_codigo():
    instancia_id = obtener_instancia()
    if not instancia_id:
        print("Error: No se encontró el servidor EC2 en ejecución.")
        return

    print(f"Iniciando despliegue seguro en la instancia {instancia_id} vía SSM...")
    
    # Comandos que se ejecutarán DENTRO del servidor EC2
    comandos = [
        'echo "--- Iniciando Despliegue Automatizado ---"',
        'sudo apt-get update -y',
        'mkdir -p /tmp/app_despliegue',
        'echo "Despliegue v1.0 completado con exito." > /tmp/app_despliegue/estado.txt',
        'echo "--- Despliegue Finalizado ---"'
    ]

    respuesta = ssm_client.send_command(
        InstanceIds=[instancia_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': comandos}
    )
    
    print(f"Comando enviado exitosamente. ID de Operación: {respuesta['Command']['CommandId']}")

if __name__ == '__main__':
    desplegar_codigo()
