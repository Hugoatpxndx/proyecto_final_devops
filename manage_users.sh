#!/bin/bash
echo "--- Configurando Usuarios y Permisos ---"

# Crear grupo de administradores
sudo groupadd cloud_admins

# Crear un usuario auditor y agregarlo al grupo
sudo useradd -m -s /bin/bash devops_auditor
sudo usermod -aG cloud_admins devops_auditor

# Crear directorio de trabajo y asignar dueño
sudo mkdir -p /opt/devops_workspace
sudo chown -R devops_auditor:cloud_admins /opt/devops_workspace

# Asignar permisos estrictos (770)
sudo chmod 770 /opt/devops_workspace

echo "Usuario 'devops_auditor' y grupo 'cloud_admins' configurados exitosamente."
