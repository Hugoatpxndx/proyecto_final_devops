import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

REGION = 'us-east-1'
MAX_LAB_INSTANCES = 9

# Inicializamos los clientes de Boto3 para los distintos servicios
ec2_client = boto3.client('ec2', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)
cw_client = boto3.client('cloudwatch', region_name=REGION)
asg_client = boto3.client('autoscaling', region_name=REGION)

def reporte_ec2_y_metricas():
    print("\n" + "="*50)
    print(" REPORTE DE INSTANCIAS EC2 Y CLOUDWATCH ")
    print("="*50)
    
    try:
        instancias = ec2_client.describe_instances()
        running_instances = []
        
        for res in instancias['Reservations']:
            for ins in res['Instances']:
                estado = ins['State']['Name']
                inst_id = ins['InstanceId']
                tipo = ins['InstanceType']
                print(f"Instancia: {inst_id} | Tipo: {tipo} | Estado: {estado}")
                
                if estado == 'running':
                    running_instances.append(inst_id)
        
        # Integración con CloudWatch: Obtener CPU de instancias en ejecución
        print("\n--- Métricas de CloudWatch (CPU Última Hora) ---")
        if not running_instances:
            print("No hay instancias en ejecución para monitorear.")
            return

        for i_id in running_instances:
            metricas = cw_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': i_id}],
                StartTime=datetime.utcnow() - timedelta(hours=1),
                EndTime=datetime.utcnow(),
                Period=3600,
                Statistics=['Average']
            )
            
            puntos = metricas.get('Datapoints', [])
            if puntos:
                cpu_promedio = puntos[0]['Average']
                print(f"Instancia {i_id} -> CPU Promedio: {cpu_promedio:.2f}%")
            else:
                print(f"Instancia {i_id} -> CPU Promedio: Datos insuficientes aún.")
                
    except ClientError as e:
        print(f"Error accediendo a EC2/CloudWatch: {e}")

def listar_s3_completo():
    print("\n" + "="*50)
    print(" INVENTARIO DE S3 (Buckets y Objetos) ")
    print("="*50)
    try:
        buckets = s3_client.list_buckets()['Buckets']
        if not buckets:
            print("No hay buckets disponibles.")
            return
            
        for bucket in buckets:
            name = bucket['Name']
            print(f"\n[Bucket] {name}")
            objs = s3_client.list_objects_v2(Bucket=name)
            
            if 'Contents' in objs:
                for obj in objs['Contents']:
                    print(f"  -> {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("  -> (Bucket vacío)")
    except ClientError as e:
        print(f"Error al acceder a S3: {e}")

def gestionar_autoescalado():
    print("\n" + "="*50)
    print(" GESTIÓN DE AUTOESCALADO (Límites Learner Lab) ")
    print("="*50)
    try:
        # Obtenemos los grupos de autoescalado actuales
        asgs = asg_client.describe_auto_scaling_groups()['AutoScalingGroups']
        
        if not asgs:
            print("No se encontraron Grupos de Autoescalado (ASG) activos en la cuenta.")
            print(f"Nota: Cualquier ASG futuro debe tener un MaxSize <= {MAX_LAB_INSTANCES} para respetar el Learner Lab.")
            return
            
        for asg in asgs:
            nombre = asg['AutoScalingGroupName']
            max_size = asg['MaxSize']
            desired = asg['DesiredCapacity']
            
            print(f"ASG Encontrado: {nombre}")
            print(f"  -> Capacidad Deseada: {desired}")
            print(f"  -> Tamaño Máximo Configurado: {max_size}")
            
            # Auditoría y Corrección Automática (Restricción del Learner Lab)
            if max_size > MAX_LAB_INSTANCES:
                print(f"  [ALERTA] El ASG excede el límite de {MAX_LAB_INSTANCES} instancias.")
                print("  [ACCIÓN] Ajustando el MaxSize automáticamente para cumplir las reglas...")
                asg_client.update_auto_scaling_group(
                    AutoScalingGroupName=nombre,
                    MaxSize=MAX_LAB_INSTANCES
                )
                print("  -> Corrección aplicada con éxito.")
            else:
                print("  -> El ASG cumple con los límites del Learner Lab. Todo en orden.")
                
    except ClientError as e:
        print(f"Error accediendo a Auto Scaling: {e}")

if __name__ == '__main__':
    reporte_ec2_y_metricas()
    listar_s3_completo()
    gestionar_autoescalado()
    print("\nScript automatizado finalizado correctamente.\n")
