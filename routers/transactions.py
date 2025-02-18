from models import auth
from database import models
from typing import Annotated
from database import schemas
from fastapi.routing import APIRouter
from contract.contract import get_contract
from sqlalchemy.exc import SQLAlchemyError
from database.database import db_dependency
from fastapi import HTTPException, status, Depends
from database.storage import load_archive_storage
from connection.code import generate_folio
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post("/order", status_code=status.HTTP_201_CREATED)
def create_order(
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
        today = datetime.today().strftime("%m%y")
        generated_folio = generate_folio(today)
        db_transaction = models.Transaction(
            customer_id=current_user.id,
            rental_start_date=transaction.rental_start_date,
            rental_end_date=transaction.rental_end_date,
            total_price=transaction.total_price,
            folio=generated_folio,
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
        # Get contract
        initial_date = transaction.rental_start_date.date()
        end_date = transaction.rental_end_date.date()
        output_path = get_contract(
            client_name=f"{current_user.name}{current_user.last_name}", 
            client_address=current_user.address,
            initial_date=initial_date, 
            end_date=end_date, 
            total_amount=transaction.total_price, 
            garantee_amount= 1500,
            folio = generated_folio
            )
        # Save contract before signing in GCS
        # path_destiny=f"users/contracts/{current_user.id}/{initial_date}/{db_transaction.id}-contract-before_signing.pdf"
        # load_archive_storage(output_path, path_destiny, current_user.email)
        db.commit()
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
    finally:
        db.close()
    
@router.put("/order/{folio}", status_code=status.HTTP_202_ACCEPTED)
def following_order( 
    db: db_dependency, 
    folio:str,
    # current_user: Annotated[dict, Depends(auth.get_current_active_user)]
    ):
    try:
        transaction = db.query(models.Transaction).filter(models.Transaction.folio == folio).first()  # Use .one() for single result
        if transaction is None: # Handle the case where the transaction isn't found
            raise HTTPException(status_code=404, detail="Transaction not found. Review the folio.")
        transaction.status = "Signed"
        db.commit()
        db.refresh(transaction)  # Refresh to get updated data from the database
        return transaction
    
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Order not found, review the folio.")
    except Exception as e: # Catch any other potential errors
        db.rollback() # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}") # Return error details.  Don't do this in production.
    finally:
        db.close()

@router.post("/order/{path}", status_code=status.HTTP_200_OK)
def get_folio_from_file_signed(path:str):
    from smtp.get_folio import get_folio_value
    import requests
    folio_value = get_folio_value(path)
    request = requests.put(f"http://127.0.0.1:8000/transactions/order/{folio_value}")
    return request.json()

@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: db_dependency):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.delete("/order/{order_id}", status_code=status.HTTP_200_OK)
def cancel_order(
    order_id:str,
    db: db_dependency,
    current_user: Annotated[dict, Depends(auth.get_current_active_user)]
    ):
    try:
        transaction = db.query(models.Transaction).filter(models.Transaction.id == order_id).first()
        if transaction is None: # Handle the case where the transaction isn't found
            raise HTTPException(status_code=404, detail="Transaction not found. Review the folio.")
        if transaction.customer_id == current_user.id:
            transaction.status = "Canceled"
            db.commit()
            db.refresh(transaction)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This order don't correspond to be yours, review the order.")  
        return transaction
            
    
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Order not found, review the folio.")
    except Exception as e: # Catch any other potential errors
        db.rollback() # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}") # Return error details.  Don't do this in production.
    finally:
        db.close()