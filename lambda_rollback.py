import json

def lambda_handler(event, context):
    print("¡ALERTA DE DESPLIEGUE FALLIDO DETECTADA!")
    print("Iniciando protocolo de Rollback automático...")
    
    # Aquí iría la lógica real para restaurar una versión anterior (ej. cambiar etiqueta en Docker o S3)
    mensaje = "Rollback ejecutado con éxito. Se ha restaurado la versión estable anterior."
    
    print(mensaje)
    
    return {
        'statusCode': 200,
        'body': json.dumps(mensaje)
    }
