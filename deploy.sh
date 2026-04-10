#!/bin/bash
echo "Iniciando despliegue de la aplicacion..."
sudo docker-compose down
sudo docker-compose up -d --build || {
    echo "Fallo el despliegue. Iniciando script de Rollback automatico..."
    sudo docker-compose down
    echo "Restaurando version anterior..."
    git reset --hard HEAD~1
    sudo docker-compose up -d --build
    echo "Rollback completado."
    exit 1
}
