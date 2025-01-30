from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de la base de datos desde las variables de entorno o por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://globantadmin:4dm1n@localhost:5432/Globant")

# Crear el motor de conexión a la base de datos
engine = create_engine(DATABASE_URL)

# Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaración base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
