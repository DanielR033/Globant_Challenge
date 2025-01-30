from fastapi import FastAPI
from app.api import transactions, csv_upload, backup_restore, metrics

# Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="Data Management API",
    description=(
        "API para manejar carga de datos, validaciones según metadata, "
        "transacciones, backups y restauraciones."
    ),
    version="1.0.0",
)

# Incluir los routers de las diferentes funcionalidades
app.include_router(transactions.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(csv_upload.router, prefix="/api/v1", tags=["CSV Management"])
app.include_router(backup_restore.router, prefix="/api/v1", tags=["Backup and Restore"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Querys"])

# Endpoint raíz para verificar el estado de la API
@app.get("/")
def root():
    """
    Verificar el estado de la API.
    """
    return {"message": "API en funcionamiento"}

