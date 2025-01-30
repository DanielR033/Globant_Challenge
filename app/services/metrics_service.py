import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from matplotlib import pyplot as plt
from io import BytesIO
import base64


class MetricsService:
    def __init__(self, db: Session):
        self.db = db

    def get_employees_per_quarter(self):
        """
        Obtiene la cantidad de empleados contratados por trimestre en 2021, agrupados por departamento y trabajo.
        """
        query = text("""
        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(he.datetime AS TIMESTAMPTZ)) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(he.datetime AS TIMESTAMPTZ)) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(he.datetime AS TIMESTAMPTZ)) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(he.datetime AS TIMESTAMPTZ)) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE EXTRACT(YEAR FROM CAST(he.datetime AS TIMESTAMPTZ)) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
        """)
        result = self.db.execute(query).fetchall()
        df = pd.DataFrame(result, columns=["department", "job", "Q1", "Q2", "Q3", "Q4"])
        return df

    def get_above_average_departments(self):
        """
        Obtiene los departamentos que contrataron más empleados que el promedio en 2021.
        """
        query = text("""
        WITH department_hires AS (
            SELECT
                d.id,
                d.department,
                COUNT(*) AS hired
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            WHERE EXTRACT(YEAR FROM CAST(he.datetime AS TIMESTAMPTZ)) = 2021
            GROUP BY d.id, d.department
        ),
        average_hires AS (
            SELECT AVG(hired) AS avg_hired FROM department_hires
        )
        SELECT dh.id, dh.department, dh.hired
        FROM department_hires dh, average_hires ah
        WHERE dh.hired > ah.avg_hired
        ORDER BY dh.hired DESC;
        """)
        result = self.db.execute(query).fetchall()
        df = pd.DataFrame(result, columns=["id", "department", "hired"])
        return df

    def generate_file(self, df: pd.DataFrame, format: str, file_name: str):
        """
        Genera un archivo en el formato especificado (json, csv, html).
        """
        file_path = f"/tmp/{file_name}"
        if format == "json":
            return df.to_dict(orient="records")
        elif format == "csv":
            df.to_csv(file_path, index=False)
            return file_path
        elif format == "html":
            df.to_html(file_path, index=False)
            return file_path
        else:
            raise ValueError("Formato no soportado. Usa 'json', 'csv' o 'html'.")
        
    def generate_employees_per_quarter_chart_in_memory(self, df: pd.DataFrame):
        """
        Genera un gráfico de barras apiladas en memoria para empleados contratados por trimestre.
        """
        import matplotlib.pyplot as plt
        import io

        # Configuración de la figura
        plt.figure(figsize=(12, 8))
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        for quarter in quarters:
            plt.bar(df["department"] + " - " + df["job"], df[quarter], label=quarter)

        plt.xlabel("Departamento - Trabajo", fontsize=12)
        plt.ylabel("Número de Contrataciones", fontsize=12)
        plt.title("Empleados Contratados por Trimestre en 2021", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.legend(title="Trimestres")
        plt.tight_layout()

        # Guardar en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)  # Reiniciar el cursor al inicio del buffer
        return buffer


    def generate_above_average_departments_chart_in_memory(self, df: pd.DataFrame):
        """
        Genera un gráfico de barras en memoria para departamentos con contrataciones por encima del promedio.
        """
        import matplotlib.pyplot as plt
        import io

        # Configuración de la figura
        plt.figure(figsize=(10, 6))
        plt.bar(df["department"], df["hired"], color="skyblue")
        plt.xlabel("Departamento", fontsize=12)
        plt.ylabel("Número de Contrataciones", fontsize=12)
        plt.title("Departamentos con Contrataciones por Encima del Promedio (2021)", fontsize=14)
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.tight_layout()

        # Guardar en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)  # Reiniciar el cursor al inicio del buffer
        return buffer



