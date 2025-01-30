import fastavro
from sqlalchemy import Table, MetaData, inspect
from sqlalchemy.orm import Session
from sqlalchemy.types import Integer, String, Float, Boolean
from app.services.csv_loader import CSVLoaderService


class BackupRestoreServices:
    def __init__(self, db: Session):
        """
        Inicializa el servicio con la sesión de la base de datos.
        """
        self.db = db
        self.engine = db.get_bind()
        self.metadata = MetaData()

    def _get_avro_type(self, sql_type):
        """
        Convierte un tipo de columna de SQLAlchemy a un tipo compatible con AVRO.
        """
        if isinstance(sql_type, Integer):
            return "int"
        elif isinstance(sql_type, String):
            return "string"
        elif isinstance(sql_type, Float):
            return "float"
        elif isinstance(sql_type, Boolean):
            return "boolean"
        else:
            raise ValueError(f"Tipo de dato no soportado para AVRO: {sql_type}.")

    def backup_table(self, table_name: str, file_path: str):
        """
        Crea un backup de una tabla específica en formato Avro.
        """

        # Validar si la tabla existe
        inspector = inspect(self.engine)
        if table_name not in inspector.get_table_names():
            raise ValueError(f"No se encontró la tabla '{table_name}'.")

        # Obtener la tabla desde la metadata
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        
        # Obtener los datos de la tabla
        rows = self.db.execute(table.select()).fetchall()

        # Extraer los nombres de las columnas
        column_names = [col.name for col in table.columns]
        print(f"Columnas detectadas: {column_names}")

        # Convertir filas a diccionarios
        try:
            formatted_rows = [dict(zip(column_names, row)) for row in rows]
            print(f"Datos formateados: {formatted_rows}")
        except Exception as e:
            raise ValueError(f"Error al formatear las filas: {e}")

        # Crear el esquema Avro con los tipos de datos adecuados
        try:
            schema = {
                "type": "record",
                "name": table_name,
                "fields": [
                    {
                        "name": col.name,
                        "type": ["null", "string"] if str(col.type) == "VARCHAR" else ["null", "int"],
                    }
                    for col in table.columns
                ],
            }
            print(f"Esquema generado: {schema}")
        except Exception as e:
            raise ValueError(f"Error al generar el esquema Avro: {e}")

        # Escribir los datos en formato Avro
        try:
            with open(file_path, "wb") as f:
                fastavro.writer(f, schema, formatted_rows)
            print(f"Backup creado exitosamente para la tabla '{table_name}' en '{file_path}'.")
        except Exception as e:
            raise ValueError(f"Error al escribir el archivo Avro: {e}")

    def restore_table(self, db, table_name: str, file_path: str):
        """
        Restaura una tabla desde un archivo AVRO.
        Si la tabla no existe, la recrea usando la metadata almacenada.
        """
        # Verificar si la tabla existe
        if not inspect(self.engine).has_table(table_name):
            print(f"La tabla '{table_name}' no existe. Intentando recrearla a partir de la metadata...")
            # Inicializar el servicio CSV con la sesión
            csv_service = CSVLoaderService(db)
            # Cargar la metadata desde el archivo
            csv_service.create_table_from_metadata(table_name)

        # Leer el archivo AVRO
        print(f"Restaurando la tabla '{table_name}' desde el archivo '{file_path}'...")
        try:
            with open(file_path, "rb") as f:
                reader = fastavro.reader(f)
                rows = list(reader)

                # Validar que hay datos para insertar
                if not rows:
                    print(f"El archivo '{file_path}' está vacío. No se restaurará nada.")
                    return

                # Obtener la tabla SQLAlchemy
                table = Table(table_name, self.metadata, autoload_with=self.engine)

                # Insertar los datos en la tabla
                with self.engine.begin() as connection:
                    connection.execute(table.insert(), rows)

                print(f"Tabla '{table_name}' restaurada exitosamente desde el archivo '{file_path}'.")
        except Exception as e:
            raise ValueError(f"Error al restaurar la tabla '{table_name}': {str(e)}")