import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.csv_loader import CSVLoaderService
from app.database.session import get_db

router = APIRouter()

@router.post("/upload-metadata/")
def upload_metadata(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Cargar la metadata desde un archivo CSV en la tabla `metadata`.
    """
    # Guardar el archivo temporalmente
    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(file.file.read())

    try:
        # Inicializar el servicio CSV con la sesión
        csv_service = CSVLoaderService(db)

        # Cargar la metadata desde el archivo
        csv_service.load_table_structures(temp_file_path)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando la metadata: {str(e)}"
        )
    finally:
        os.remove(temp_file_path)

    return {"message": f"Metadata cargada correctamente desde {file.filename}."}

@router.post("/upload-csv/")
def upload_multiple_csv(
    files: list[UploadFile] = File(...),  # Acepta múltiples archivos CSV
    db: Session = Depends(get_db)
):
    """
    Endpoint para cargar múltiples archivos CSV en las tablas definidas por la metadata.
    """
    try:
        csv_service = CSVLoaderService(db)  # Servicio de carga de CSV

        results = []  # Para almacenar el estado de cada archivo

        for file in files:
            temp_file_path = f"/tmp/{file.filename}"  # Ruta temporal para cada archivo
            with open(temp_file_path, "wb") as f:
                f.write(file.file.read())

            try:
                csv_service.load_csv_to_table(temp_file_path)  # Cargar en la base de datos
                results.append({"filename": file.filename, "status": "success"})
            except Exception as e:
                results.append({"filename": file.filename, "status": "error", "detail": str(e)})
            finally:
                os.remove(temp_file_path)  # Eliminar archivo temporal

        return {"results": results}  # Devuelve un informe para todos los archivos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando los archivos CSV: {str(e)}")

