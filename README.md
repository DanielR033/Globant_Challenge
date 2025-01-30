# Proyecto de Gestión de Datos y Métricas

Este proyecto tiene como objetivo construir un sistema de gestión de datos y métricas utilizando FastAPI, PostgreSQL y otras herramientas modernas para facilitar la carga, exploración, visualización y respaldo de datos.

## Estructura del Proyecto

El proyecto sigue una estructura de carpetas organizada:

```
Proyecto/
├── api/
│   ├── csv_upload.py
│   ├── metrics.py
│   ├── backup_restore.py
├── database/
│   ├── session.py
│   ├── models.py
├── services/
│   ├── csv_loader_service.py
│   ├── metrics_service.py
│   ├── backup_restore_service.py
├── static/
│   └── charts/  # Carpeta para guardar gráficos generados
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Funcionalidades

### 1. Gestión de Carga de Datos
- **Cargar Metadata:** Permite cargar la estructura de las tablas desde un archivo CSV para crear dinámicamente las tablas en la base de datos.
- **Cargar Datos:** Permite cargar datos en las tablas existentes desde archivos CSV.

### 2. Respaldo y Restauración
- **Backup de Tablas:** Genera un respaldo de las tablas en formato Avro.
- **Restaurar Tablas:** Restaura datos en las tablas desde archivos de respaldo.

### 3. Generación de Métricas y Reportes
- **Métricas de Contrataciones por Trimestre:**
  - Genera una tabla con el número de empleados contratados por departamento y puesto, ordenada por trimestre.
  - Exporta los resultados en formato JSON, CSV o gráficos de barras descargables.
- **Departamentos con Contrataciones por Encima del Promedio:**
  - Identifica los departamentos que contrataron más empleados que el promedio.
  - Exporta los resultados en formato JSON, CSV o gráficos de barras descargables.

## Requisitos del Sistema

- Python 3.9+
- PostgreSQL 12+
- Docker y Docker Compose

## Configuración e Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/proyecto.git
   cd proyecto
   ```

2. **Configurar el entorno**
   - Crear un archivo `.env` con las variables de entorno necesarias.
   ```env
   DATABASE_URL=postgresql+psycopg2://globantadmin:4dm1n@postgres:5432/Globant
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Construir y levantar contenedores**
   ```bash
   docker-compose up --build
   ```

5. **Acceder a la API**
   - La API estará disponible en `http://localhost:8000`.
   - La documentación interactiva se encuentra en `http://localhost:8000/docs`.

## Despliegue en la nube

### Despliegue en AWS usando Lambda

1. **Preparar el entorno**:
   - Empaqueta la aplicación junto con sus dependencias en un archivo ZIP.
   ```bash
   zip -r deployment-package.zip .
   ```

2. **Subir el paquete a AWS Lambda**:
   - Crea una función Lambda desde la consola de AWS y sube el archivo ZIP.

3. **Configurar API Gateway**:
   - Configura un API Gateway para exponer tu Lambda como una API REST.

4. **Probar el endpoint**:
   - Obtén la URL de API Gateway y verifica que la API esté funcionando correctamente.

---

### Despliegue en AWS usando EC2

1. **Lanzar una instancia EC2**:
   - Elige una imagen AMI de Amazon Linux y configura el tamaño de la instancia.

2. **Configurar el entorno en EC2**:
   ```bash
   sudo yum update -y
   sudo yum install docker git python3-pip -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

3. **Clonar y ejecutar el proyecto**:
   ```bash
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DEL-PROYECTO>
   docker-compose up --build
   ```

4. **Configurar el acceso**:
   - Asegúrate de abrir el puerto 8000 en el grupo de seguridad de la instancia.

5. **Acceder a la API**:
   - Usa la dirección IP pública de tu instancia para acceder a la API.

---

### Despliegue en Azure usando App Service

1. **Instalar la CLI de Azure**:
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Iniciar sesión en Azure**:
   ```bash
   az login
   ```

3. **Crear un grupo de recursos**:
   ```bash
   az group create --name <nombre-del-grupo> --location <región>
   ```

4. **Crear un plan de App Service**:
   ```bash
   az appservice plan create --name <nombre-del-plan> --resource-group <nombre-del-grupo> --sku FREE
   ```

5. **Crear una App Service para tu aplicación**:
   ```bash
   az webapp create --resource-group <nombre-del-grupo> --plan <nombre-del-plan> --name <nombre-de-la-app> --runtime "PYTHON:3.9"
   ```

6. **Desplegar la aplicación usando Git**:
   ```bash
   az webapp deployment source config-local-git --name <nombre-de-la-app> --resource-group <nombre-del-grupo>
   ```
   Obtendrás una URL para el repositorio Git de tu App Service.

7. **Configurar tu repositorio y desplegar**:
   ```bash
   git remote add azure <url-del-repositorio-git>
   git push azure master
   ```

8. **Acceder a tu aplicación**:
   La aplicación estará disponible en `<nombre-de-la-app>.azurewebsites.net`.

---

## Uso de la API

### Endpoints Principales

#### Gestión de Datos
- **Subir Metadata:**
  ```http
  POST /api/v1/upload-metadata/
  ```
- **Cargar Datos:**
  ```http
  POST /api/v1/upload-csv/
  ```

#### Respaldo y Restauración
- **Crear Backup:**
  ```http
  POST /api/v1/backup/{table_name}/
  ```
- **Restaurar Tabla:**
  ```http
  POST /api/v1/restore/{table_name}/
  ```

#### Métricas
- **Contrataciones por Trimestre:**
  ```http
  GET /api/v1/metrics/employees-per-quarter/
  ```
- **Departamentos con Contrataciones por Encima del Promedio:**
  ```http
  GET /api/v1/metrics/above-average-departments/
  ```

## Generación de Gráficos

Los gráficos se generan dinámicamente y se pueden descargar como archivos PNG. Están disponibles en los siguientes endpoints:

- **Gráfico de Contrataciones por Trimestre:**
  ```http
  GET /api/v1/metrics/employees-per-quarter/chart
  ```
- **Gráfico de Departamentos con Contrataciones por Encima del Promedio:**
  ```http
  GET /api/v1/metrics/above-average-departments/chart
  ```
