from fastapi.routing import APIRouter
from typing import Annotated
from datetime import timedelta
from fastapi import Request, HTTPException, status, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import crud, auth
from database import schemas
from database.database import db_dependency
from jose import  JWTError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import models
from database.storage import load_archive_storage

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    db: db_dependency, 
    current_user: Annotated[dict, Depends(auth.get_current_active_user)]
    ):
    # Create the transaction
    try:
        # Validate all products exist
        for product in transaction.products:
            product_in_db = db.query(models.Item).filter(models.Item.id == product.item_id).first()
            if not product_in_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {product.item_id} does not exist."
                )

        # Create the transaction
        db_transaction = models.Transaction(
            customer_id=current_user.id,
            rental_start_date=transaction.rental_start_date,
            rental_end_date=transaction.rental_end_date,
            total_price=transaction.total_price,
            status=transaction.status,
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        # Add products to the transaction
        for product in transaction.products:
            db_transaction_product = models.TransactionItem(
                transaction_id=db_transaction.id,
                item_id=product.item_id,
                quantity=product.quantity,
            )
            db.add(db_transaction_product)

        db.commit()
        date = transaction.rental_start_date.date()
        file = "C:/Users/ARCAN/OneDrive/Escritorio/Documentos/Software/VideoProductora/src/curriculum.pdf"
        path_destiny=f"users/contracts/{current_user.id}/{date}/{db_transaction.id}-contract.pdf"
        load_archive_storage(file, path_destiny)
        return transaction

    except HTTPException as e:
        # Explicit validation error raised during product checks
        db.rollback()
        raise e

    except SQLAlchemyError as e:
        # Handle unexpected database errors
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the transaction. Please try again."
        )

@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: db_dependency):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction