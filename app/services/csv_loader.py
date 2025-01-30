import os
from datetime import datetime
import pandas as pd
from sqlalchemy import inspect, Table, Column, Integer, String, MetaData, Boolean, ForeignKey
from sqlalchemy.orm import Session
from app.database.models import Metadata

class CSVLoaderService:
    def __init__(self, db: Session):
        """
        Inicializa el servicio con la sesión de la base de datos.
        """
        self.db = db
        self.engine = db.get_bind()
        self.metadata = MetaData()

    def create_metadata_table(self):
        """
        Crea la tabla de metadata si no existe.
        """
        if not inspect(self.engine).has_table("metadata"):
            metadata_table = Table(
                "metadata",
                self.metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),  # Clave primaria autoincrementada
                Column("table_name", String, nullable=False),  # No puede ser nulo
                Column("column_name", String, nullable=False),  # No puede ser nulo
                Column("data_type", String, nullable=False),  # No puede ser nulo
                Column("is_primary_key", Boolean, nullable=False, default=False),
                Column("is_foreign_key", Boolean, nullable=False, default=False),
                Column("foreign_table", String, nullable=True),  # Puede ser nulo
                Column("foreign_column", String, nullable=True),  # Puede ser nulo
            )
            self.metadata.create_all(self.engine)
            print("Tabla 'metadata' creada correctamente.")
        else:
            print("La tabla 'metadata' ya existe.")

    def load_table_structures(self, structure_file: str):
        """
        Carga la metadata desde un archivo CSV en la tabla 'metadata'.
        """
        data = pd.read_csv(structure_file)

        # Asegúrate de que la tabla de metadata exista
        self.create_metadata_table()

        # Insertar los datos en la tabla 'metadata'
        for _, row in data.iterrows():
            metadata_entry = Metadata(
                table_name=row["table_name"],
                column_name=row["column_name"],
                data_type=row["data_type"],
                is_primary_key=bool(row["is_primary_key"]),
                is_foreign_key=bool(row["is_foreign_key"]),
                foreign_table=row["foreign_table"] if pd.notna(row["foreign_table"]) else None,
                foreign_column=row["foreign_column"] if pd.notna(row["foreign_column"]) else None,
            )
            self.db.add(metadata_entry)

        self.db.commit()
        print("Metadata cargada correctamente.")

    def create_table_from_metadata(self, table_name: str):
        """
        Crea una tabla en la base de datos basada en la metadata.
        """
        # Actualizar metadata
        self.metadata.reflect(bind=self.engine)

        if inspect(self.engine).has_table(table_name):
            print(f"La tabla '{table_name}' ya existe.")
            return

        # Obtener metadata para la tabla
        metadata_entries = self.db.query(Metadata).filter(Metadata.table_name == table_name).all()
        columns = []

        print(f"Creando tabla '{table_name}'...")
        for entry in metadata_entries:
            column_type = String if entry.data_type == "STRING" else Integer
            kwargs = {}

            # Configurar llave primaria
            if entry.is_primary_key:
                kwargs["primary_key"] = True
                print(f" - Columna '{entry.column_name}' marcada como PRIMARY KEY.")

            # Configurar llave foránea
            if entry.is_foreign_key:
                foreign_table = entry.foreign_table
                foreign_column = entry.foreign_column

                # Verifica si la tabla referenciada existe
                if not inspect(self.engine).has_table(foreign_table):
                    print(f"Tabla referenciada '{foreign_table}' no encontrada. Creándola primero.")
                    self.create_table_from_metadata(foreign_table)

                foreign_key = ForeignKey(f"{foreign_table}.{foreign_column}")
                print(f" - Columna '{entry.column_name}' tendrá FOREIGN KEY -> {foreign_table}({foreign_column}).")
                column = Column(entry.column_name, column_type, foreign_key, **kwargs)
            else:
                column = Column(entry.column_name, column_type, **kwargs)

            columns.append(column)

        # Crear la tabla
        table = Table(table_name, self.metadata, *columns)
        try:
            print(f" - Ejecutando creación de la tabla '{table_name}' con las columnas:")
            for col in columns:
                print(f"   > {col.name} ({col.type}) {'PRIMARY KEY' if col.primary_key else ''}")
            self.metadata.create_all(self.engine)
            print(f"Tabla '{table_name}' creada correctamente.")
        except Exception as e:
            print(f"Error al crear la tabla '{table_name}': {str(e)}")
            raise

    def load_csv_to_table(self, csv_path: str):
        """
        Carga datos desde un archivo CSV en una tabla específica, creando la tabla si no existe basada en la metadata.
        """
        # Leer datos del archivo CSV
        data = pd.read_csv(csv_path, header=None)

        # Determinar la tabla a la que pertenece
        table_name = os.path.splitext(os.path.basename(csv_path))[0].lower()

        # Validar si la tabla existe y crearla si es necesario
        inspector = inspect(self.engine)
        if table_name not in inspector.get_table_names():
            print(f"La tabla '{table_name}' no existe. Creándola a partir de la metadata...")
            self.create_table_from_metadata(table_name)

        # Obtener las columnas desde la metadata
        metadata_entries = self.db.query(Metadata).filter(Metadata.table_name == table_name).all()
        columns = [entry.column_name for entry in metadata_entries]

        if len(columns) != data.shape[1]:
            raise ValueError(f"El número de columnas en el archivo ({data.shape[1]}) no coincide con la metadata ({len(columns)}).")

        # Asignar nombres de columnas basados en la metadata
        data.columns = columns

        # Insertar los datos en la tabla
        data.to_sql(table_name, self.engine, if_exists="append", index=False)
        print(f"Datos cargados exitosamente en la tabla '{table_name}'.")

