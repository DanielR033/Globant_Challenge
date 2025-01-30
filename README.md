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

## Tests

Para ejecutar las pruebas del proyecto:
```bash
pytest
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con tus sugerencias.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

