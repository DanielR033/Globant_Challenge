from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.metrics_service import MetricsService
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, Response

router = APIRouter()

@router.get("/metrics/employees-per-quarter")
def employees_per_quarter(format: str = "json", db: Session = Depends(get_db)):
    """
    Endpoint para generar un reporte de empleados contratados por trimestre en 2021.
    """
    try:
        metrics_service = MetricsService(db)
        df = metrics_service.get_employees_per_quarter()

        if format == "json":
            data = metrics_service.generate_file(df, format, "employees_per_quarter.json")
            return JSONResponse(content=data)
        elif format in ["csv", "html"]:
            file_path = metrics_service.generate_file(df, format, f"employees_per_quarter.{format}")
            return FileResponse(file_path, media_type=f"text/{format}", filename=f"employees_per_quarter.{format}")
        else:
            raise HTTPException(status_code=400, detail="Formato no soportado. Usa 'json', 'csv' o 'html'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando métricas: {str(e)}")



@router.get("/metrics/above-average-departments")
def above_average_departments(format: str = "json", db: Session = Depends(get_db)):
    """
    Endpoint para generar un reporte de departamentos que contrataron más empleados que el promedio.
    """
    try:
        metrics_service = MetricsService(db)
        df = metrics_service.get_above_average_departments()

        if format == "json":
            data = metrics_service.generate_file(df, format, "above_average_departments.json")
            return JSONResponse(content=data)
        elif format in ["csv", "html"]:
            file_path = metrics_service.generate_file(df, format, f"above_average_departments.{format}")
            return FileResponse(file_path, media_type=f"text/{format}", filename=f"above_average_departments.{format}")
        else:
            raise HTTPException(status_code=400, detail="Formato no soportado. Usa 'json', 'csv' o 'html'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando métricas: {str(e)}")
    
@router.get("/metrics/employees-per-quarter/chart")
def employees_per_quarter_chart(db: Session = Depends(get_db)):
    """
    Genera un gráfico de barras para empleados contratados por trimestre en 2021 y lo devuelve para descarga.
    """
    try:
        metrics_service = MetricsService(db)
        df = metrics_service.get_employees_per_quarter()
        buffer = metrics_service.generate_employees_per_quarter_chart_in_memory(df)

        headers = {
            "Content-Disposition": "attachment; filename=employees_per_quarter_chart.png"
        }
        return Response(buffer.getvalue(), media_type="image/png", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando el gráfico: {str(e)}")


@router.get("/metrics/above-average-departments/chart")
def above_average_departments_chart(db: Session = Depends(get_db)):
    """
    Genera un gráfico de barras para departamentos con contrataciones por encima del promedio en 2021 y lo devuelve para descarga.
    """
    try:
        metrics_service = MetricsService(db)
        df = metrics_service.get_above_average_departments()
        buffer = metrics_service.generate_above_average_departments_chart_in_memory(df)

        headers = {
            "Content-Disposition": "attachment; filename=above_average_departments_chart.png"
        }
        return Response(buffer.getvalue(), media_type="image/png", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando el gráfico: {str(e)}")


