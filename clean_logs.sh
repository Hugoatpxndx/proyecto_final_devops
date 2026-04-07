#!/bin/bash

echo "Iniciando limpieza de logs..."

# Busca y elimina archivos .log más viejos de 7 días en /var/log
sudo find /var/log -type f -name "*.log" -mtime +7 -exec rm -f {} \;

# Guarda un registro de la acción
echo "Limpieza completada el: $(date)" >> /home/ubuntu/historial_limpieza.txt
