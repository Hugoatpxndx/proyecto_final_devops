# Proyecto Final DevOps - Soluciones Tecnológicas del Futuro

Plataforma automatizada de despliegue y monitoreo en AWS, implementando prácticas de DevOps para optimizar la entrega de software en el sector financiero.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Automatización con Scripts](#-automatización-con-scripts)
- [Infraestructura como Código](#-infraestructura-como-código)
- [Contenedores Docker](#-contenedores-docker)
- [CI/CD con AWS CodePipeline](#-cicd-con-aws-codepipeline)
- [Monitoreo](#-monitoreo)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 📖 Descripción del Proyecto

Este proyecto implementa una plataforma DevOps completa para **Soluciones Tecnológicas del Futuro**, una empresa de desarrollo de aplicaciones web para el sector financiero.

### Objetivos

- **Automatizar** el proceso de despliegue para reducir tareas manuales
- **Mejorar** la estabilidad y confiabilidad de las aplicaciones
- **Garantizar** la seguridad de la infraestructura en la nube
- **Optimizar** los tiempos de entrega mediante CI/CD

### Principios DevOps Implementados

| Principio | Implementación |
|-----------|----------------|
| Automatización | Scripts Bash, Python con Boto3, CloudFormation |
| Colaboración | Metodología Agile, PR reviews, branch protection |
| Medición | AWS CloudWatch para métricas y monitoreo |
| DevSecOps | SonarQube para escaneo de vulnerabilidades |
| CI/CD | AWS CodePipeline para despliegue continuo |
| Pruebas automatizadas | CodeBuild con tests automatizados |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  CodeCommit  │→ │  CodeBuild   │→ │    CodePipeline      │   │
│  │   (Repo)     │  │   (Tests)    │  │   (Orchestration)    │   │
│  └──────────────┘  └──────────────┘  └──────────┬───────────┘   │
│                                                  │               │
│  ┌──────────────┐  ┌──────────────┐              │               │
│  │     S3       │  │  CloudWatch │←─────────────┘               │
│  │  (Storage)   │  │ (Monitoring)│                               │
│  └──────────────┘  └──────────────┘                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     VPC Network                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │   │
│  │  │    EC2     │  │    EC2     │  │       Lambda       │  │   │
│  │  │ (Instance)  │  │ (Instance)  │  │   (Rollback)       │  │   │
│  │  └────────────┘  └────────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
proyecto_final_devops/
├── .github/                      # Configuración de GitHub Actions
├── aws_automation.py             # Script Python para automatización AWS
├── clean_logs.sh                 # Script de limpieza de logs (cron)
├── deploy.sh                     # Script de despliegue con rollback
├── docker-compose.yml            # Orquestación de contenedores
├── Dockerfile                    # Imagen Docker multi-stage
├── install_dependencies.sh       # Instalación de dependencias
├── infraestructura.yaml          # Plantilla CloudFormation
├── README.md                     # Este archivo
└── .gitignore                    # Archivos ignorados por Git
```

---

## 📦 Requisitos

### Herramientas Locales

- Git 2.0+
- Python 3.8+
- Docker 20.10+
- Docker Compose 1.29+
- AWS CLI v2

### Servicios AWS

- AWS Account con permisos (LabRole)
- AWS CodeCommit
- AWS CodeBuild
- AWS CodePipeline
- AWS EC2 (t2.micro, máximo 9 instancias)
- AWS S3
- AWS CloudWatch
- AWS Lambda

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/USUARIO/proyecto_final_devops.git
cd proyecto_final_devops
```

### 2. Configurar Git

```bash
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

### 3. Instalar Dependencias (Linux/Ubuntu)

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### 4. Configurar AWS CLI

```bash
aws configure
# Ingresar Access Key, Secret Key, region: us-east-1
```

---

## 📖 Uso

### Scripts Bash

#### Instalación de Dependencias

```bash
./install_dependencies.sh
```

#### Despliegue con Rollback Automático

```bash
chmod +x deploy.sh
./deploy.sh
```

#### Limpieza de Logs (Programado con cron)

```bash
# Agregar al crontab para ejecutar diariamente a las 2:00 AM
crontab -e
# 0 2 * * * /path/to/clean_logs.sh
```

### Script Python (AWS Automation)

```bash
# Generar reporte de recursos
python3 aws_automation.py

# Aprovisionar instancias EC2 (máximo 9 en Learner Lab)
# Descomentar la línea en aws_automation.py y ejecutar:
python3 aws_automation.py
```

### Docker

```bash
# Construir y ejecutar contenedores
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

---

## 🔧 Automatización con Scripts

### Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `install_dependencies.sh` | Instala git, vim, docker, python3 |
| `deploy.sh` | Despliega con rollback automático |
| `clean_logs.sh` | Limpia logs mayores a 7 días |

### Programación con Cron

```bash
# Editar crontab
crontab -e

# Limpieza de logs diaria a las 2:00 AM
0 2 * * * /home/ubuntu/clean_logs.sh >> /var/log/cron_limpieza.log 2>&1

# Reiniciar servicios semanalmente
0 3 * * 0 /home/ubuntu/restart_services.sh
```

---

## ☁️ Infraestructura como Código

### CloudFormation

Despliega infraestructura en AWS:

```bash
# Crear stack
aws cloudformation create-stack \
  --stack-name ProyectoDevOps \
  --template-body file://infraestructura.yaml \
  --region us-east-1

# Actualizar stack
aws cloudformation update-stack \
  --stack-name ProyectoDevOps \
  --template-body file://infraestructura.yaml \
  --region us-east-1

# Ver recursos
aws cloudformation describe-stacks --stack-name ProyectoDevOps
```

### Recursos Desplegados

- **EC2 Instance**: t2.micro (ServidorIaC-Proyecto)
- **S3 Bucket**: Con versionado habilitado

---

## 🐳 Contenedores Docker

### Dockerfile (Multi-stage Build)

```dockerfile
# Stage 1: Builder
FROM alpine:latest AS builder
WORKDIR /app
RUN echo "<h1>App</h1>" > index.html

# Stage 2: Production
FROM nginx:alpine
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

Servicios orquestados:

- **web**: Servidor nginx con la aplicación
- **db**: Redis para caché de datos

```bash
# Iniciar todos los servicios
docker-compose up -d

# Escalar servicios
docker-compose up -d --scale web=3
```

---

## 🔄 CI/CD con AWS CodePipeline

### Pipeline Flow

```
CodeCommit → CodeBuild → CodeDeploy → CloudWatch
   │            │            │            │
   │        Tests &      Deploy to      Monitoring
   │        Build         EC2 via SSM   & Alerts
```

### Configuración

1. **CodeCommit**: Repositorio Git privado
2. **CodeBuild**: Compilación y pruebas
3. **CodePipeline**: Orquestación del flujo
4. **Systems Manager**: Deploy a EC2

### Lambda para Rollback

Función que detecta fallos y ejecuta rollback automático:

```python
import boto3

def lambda_handler(event, context):
    codepipeline = boto3.client('codepipeline')
    # Detecta fallo y restaura versión anterior
```

---

## 📊 Monitoreo

### AWS CloudWatch

- **Métricas**: CPU, memoria, red
- **Logs**: Centralización de logs
- **Alarmas**: Notificaciones SNS

### Configurar Alarmas

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name HighCPU \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

---

## 🔐 Seguridad

### Prácticas DevSecOps

- Escaneo de vulnerabilidades con SonarQube
- Políticas IAM con privilegio mínimo
- Secrets management en AWS Secrets Manager
- HTTPS/TLS en todos los endpoints

### Protección de Ramas

- Required PR reviews
- Branch protection en main
- Status checks obligatorios

---

## 📝 Convenciones de Commits

Usar prefijos para categorizar cambios:

```
feat:     Nueva funcionalidad
fix:      Corrección de bugs
docs:     Documentación
style:    Formato (sin cambio de código)
refactor: Refactorización
test:     Pruebas
chore:    Tareas de mantenimiento
```

Ejemplo:
```bash
git commit -m "feat: agregar script de rollback automático"
git commit -m "fix: corregir path en Dockerfile"
git commit -m "docs: actualizar README con nuevas secciones"
```

---

## 👥 Contribución

1. Crear branch desde `develop`: `git checkout -b feature/nueva-funcion`
2. Hacer commits siguiendo convenciones
3. Abrir Pull Request hacia `develop`
4. Esperar revisión y aprobación
5. Mergear después de approval

---

## 📄 Licencia

Este proyecto es parte del curso de DevOps de Soluciones Tecnológicas del Futuro.

---

## 👨‍💻 Autor

**Soluciones Tecnológicas del Futuro** - Proyecto Final DevOps

---

<p align="center">
  <img src="https://img.shields.io/badge/DevOps-Implemented-blue" alt="DevOps">
  <img src="https://img.shields.io/badge/AWS-CloudFormation-orange" alt="AWS">
  <img src="https://img.shields.io/badge/Docker-Containerized-blue" alt="Docker">
  <img src="https://img.shields.io/badge/CI%2FCD-CodePipeline-green" alt="CI/CD">
</p>
