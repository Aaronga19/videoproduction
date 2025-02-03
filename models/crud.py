from sqlalchemy.orm import Session
from database import models, schemas
from bcrypt import hashpw, gensalt, checkpw
from .auth import hash_password, verify_password

# User
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.Customer.email == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if user and verify_password(password, user.password):
        return user
    return None

# Customer
def get_customer_by_email(db: Session, email: str):
    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    print(customer)
    return customer
    
def get_customer_by_id(db: Session, id: str):
    return db.query(models.Customer).filter(models.Customer.id == id).first()

def get_customer_by_username(db: Session, username: str):
    return db.query(models.Customer).filter(models.Customer.username == username).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    hashed_password = hash_password(customer.password)
    db_customer = models.Customer(
        name = customer.name,
        last_name = customer.last_name,
        email = customer.email,
        password = hashed_password,
        address = customer.address,
        zip_code = customer.zip_code,
        company = customer.company
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Authenticate a user
def authenticate_customer(db: Session, email: str, password: str):
    customer = get_customer_by_email(db, email=email)
    if customer and verify_password(password, customer.password):
        return customer
    return None



def delete_customer(db: Session, email: str):
    print(db,email)
    customer = get_customer_by_email(db, email)
    db.delete(customer)
    db.commit()

def update_customer(db: Session, id: int, address: str, company:str):
    customer = get_customer_by_id(db, id)
    customer.address = address
    customer.company = company
    db.commit()
    db.refresh(customer)
    return customer


# Items
def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name = item.name,
        type = item.type,
        description = item.description,
        category = item.category,
        price = item.price,
        proportions = item.proportions,
        model = item.model,
        images = item.images,
        manufacturer =  item.manufacturer,
        stock = item.stock,
        daily_rate = item.daily_rate,
        availability = item.availability
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Transactions
def create_transaction(db: Session, transaction: schemas.TransactionBase):
    db_transaction = models.transaction(
        customer_id = transaction.customer_id,
        comentaries = transaction.comentaries,
        owner = transaction.owner,
        items = transaction.items,
        amount = transaction.amount,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

