from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Date, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class TransactionItem(Base):
    __tablename__ = 'transaction_items'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)  # Quantity of product rented

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="employee")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    company = Column(String, nullable=True)
    role = Column(String, default="customer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Item(Base):
    __tablename__ = "items"

    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    price = Column(String, nullable=False)
    stock = Column(String, nullable=True)
    proportions = Column(String, nullable=True)
    model = Column(String, nullable=True)
    daily_rate = Column(DECIMAL(10, 2), nullable=False)
    images = Column(String, nullable=True)
    status = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    availability = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    transactions = relationship("Transaction", secondary="transaction_items", back_populates="items")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    rental_start_date = Column(TIMESTAMP, nullable=False)
    rental_end_date = Column(TIMESTAMP, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String, nullable=False, default='Pending')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer")
    items = relationship("Item", secondary="transaction_items", back_populates="transactions")
    payments = relationship("Payment", back_populates="transaction")


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    payment_date = Column(TIMESTAMP, server_default=func.now())
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False, default='Pending')  # Pending, Completed, Failed

    transaction = relationship("Transaction", back_populates="payments")
