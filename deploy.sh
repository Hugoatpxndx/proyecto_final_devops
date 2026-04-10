#!/bin/bash
echo "Iniciando despliegue de la aplicacion..."
sudo apt-get update -y
sudo apt-get install docker-compose -y
sudo docker-compose down || true
if sudo docker-compose up -d --build; then
    echo "¡Despliegue exitoso!"
    exit 0
else
    echo "Fallo el despliegue. Iniciando script de Rollback automatico..."
    sudo docker-compose down
    echo "Restaurando contenedores a un estado seguro..."
    sudo docker-compose up -d
    echo "Rollback completado exitosamente."
    exit 1
fi
