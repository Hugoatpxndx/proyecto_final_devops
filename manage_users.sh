#!/bin/bash
echo "--- Configurando Usuarios y Permisos ---"
sudo groupadd cloud_admins
sudo useradd -m -s /bin/bash devops_auditor
sudo usermod -aG cloud_admins devops_auditor
sudo mkdir -p /opt/devops_workspace
sudo chown -R devops_auditor:cloud_admins /opt/devops_workspace
sudo chmod 770 /opt/devops_workspace
echo "Usuario y grupo configurados."
