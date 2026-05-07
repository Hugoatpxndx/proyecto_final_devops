# ==========================================
# Etapa 1: Construcción (Builder)
# ==========================================
FROM alpine:latest AS builder
WORKDIR /app

# Simulamos un proceso de compilación/generación de archivos de nuestra app
RUN echo "<!DOCTYPE html><html><head><title>Proyecto DevOps</title><style>body { font-family: Arial; text-align: center; margin-top: 50px; }</style></head><body><h1>Soluciones Tecnologicas del Futuro</h1><p>Aplicacion web corriendo en Nginx optimizada con Multi-Stage Build.</p></body></html>" > index.html

# ==========================================
# Etapa 2: Producción
# ==========================================
FROM nginx:alpine

# Copiamos ÚNICAMENTE el archivo generado desde la etapa 'builder'
# Esto deja atrás cualquier herramienta de compilación, reduciendo el tamaño de la imagen.
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html

# Exponemos el puerto estándar de Nginx
EXPOSE 80
