from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

# Modelo para la tabla de transacciones
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)

# Modelo para la tabla de metadata
class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    table_name = Column(String, index=True, nullable=False)
    column_name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    is_primary_key = Column(Boolean, default=False)
    is_foreign_key = Column(Boolean, default=False)
    foreign_table = Column(String, nullable=True)
    foreign_column = Column(String, nullable=True)
