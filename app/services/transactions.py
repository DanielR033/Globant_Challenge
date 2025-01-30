from sqlalchemy.orm import Session
from app.database.models import Transaction
from app.schemas.transactions import TransactionBase

def insert_transaction(db: Session, transaction: TransactionBase):
    """
    Inserta una transacción individual en la base de datos.
    """
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def insert_batch(db: Session, transactions: list[TransactionBase]):
    """
    Inserta un lote de transacciones en la base de datos.
    """
    db_transactions = [Transaction(**t.dict()) for t in transactions]
    db.add_all(db_transactions)
    db.commit()
