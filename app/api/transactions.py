from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transactions import TransactionBase, TransactionBatch
from app.services.transactions import insert_transaction, insert_batch
from app.database.session import get_db

router = APIRouter()

@router.post("/transactions/")
def create_transaction(transaction: TransactionBase, db: Session = Depends(get_db)):
    """
    Endpoint para crear una transacción individual.
    """
    try:
        result = insert_transaction(db, transaction)
        return {"message": "Transacción creada con éxito.", "transaction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando la transacción: {str(e)}")

@router.post("/transactions/batch/")
def create_batch(transactions: TransactionBatch, db: Session = Depends(get_db)):
    """
    Endpoint para crear un lote de transacciones (1 a 1000 transacciones).
    """
    if len(transactions.transactions) > 1000:
        raise HTTPException(
            status_code=400,
            detail="El lote excede el límite máximo de 1000 transacciones."
        )

    try:
        insert_batch(db, transactions.transactions)
        return {"message": f"Lote de {len(transactions.transactions)} transacciones creado con éxito."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando el lote de transacciones: {str(e)}")
