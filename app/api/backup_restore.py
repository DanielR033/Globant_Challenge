from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.backup_restore_services import BackupRestoreServices
from app.database.session import get_db

router = APIRouter()

@router.post("/backup/{table_name}/")
def backup_table_endpoint(table_name: str, db: Session = Depends(get_db)):
    """
    Endpoint para realizar un backup de una tabla específica en formato Avro.
    """
    file_path = f"/tmp/{table_name}_backup.avro"
    try:
        # Realizar el backup de la tabla
        backup_service = BackupRestoreServices(db)
        backup_service.backup_table(table_name, file_path)
        
        return {"message": f"Backup de la tabla '{table_name}' creado exitosamente.", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando el backup: {str(e)}")

@router.post("/restore/{table_name}/")
def restore_table_endpoint(table_name: str, db: Session = Depends(get_db)):
    """
    Endpoint para restaurar una tabla desde un archivo de backup en formato Avro.
    """
    file_path = f"/tmp/{table_name}_backup.avro"
    try:
        # Restaurar la tabla desde el backup
        backup_service = BackupRestoreServices(db)
        backup_service.restore_table(db,table_name, file_path)
        return {"message": f"Tabla '{table_name}' restaurada exitosamente desde el backup.", "file_path": file_path}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No se encontró el archivo de backup para la tabla '{table_name}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restaurando la tabla: {str(e)}")

