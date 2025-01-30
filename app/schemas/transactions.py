from pydantic import BaseModel
from typing import List

class TransactionBase(BaseModel):
    """
    Esquema para una transacción individual.
    """
    amount: float
    description: str

    class Config:
        orm_mode = True  # Habilitar compatibilidad con SQLAlchemy

class TransactionBatch(BaseModel):
    """
    Esquema para un lote de transacciones.
    """
    transactions: List[TransactionBase]
