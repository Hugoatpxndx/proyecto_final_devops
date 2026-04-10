#!/bin/bash
echo "Iniciando despliegue de la aplicacion..."

# Intenta construir y levantar los nuevos contenedores
if sudo docker-compose up -d --build; then
    echo "Despliegue exitoso."
else
    echo "Fallo el despliegue. Iniciando script de Rollback automatico..."
    # Detiene contenedores fallidos
    sudo docker-compose down
    # Restaura los contenedores a su ultimo estado estable
    echo "Restaurando version anterior..."
    sudo docker-compose up -d
    echo "Rollback completado."
    exit 1
fi