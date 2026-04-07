#!/bin/bash

echo "Actualizando la lista de paquetes del sistema..."
sudo apt update -y

echo "Instalando Git, Vim y Python3..."
sudo apt install -y git vim python3 python3-pip

echo "Instalando Docker..."
sudo apt install -y docker.io

echo "Habilitando e iniciando el servicio de Docker..."
sudo systemctl enable docker
sudo systemctl start docker

# Agregamos el usuario 'ubuntu' al grupo docker para no usar sudo siempre
sudo usermod -aG docker ubuntu

echo "=========================================="
echo "¡Instalación completada con éxito!"
echo "Versiones instaladas:"
git --version
python3 --version
docker --version
echo "=========================================="
Automatizar la instalación de dependencias.
Programar tareas con cron para limpieza de logs.
