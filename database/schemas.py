from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
# Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    role: str = "employee"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Customer
class CustomerBase(BaseModel): 
    email: EmailStr
    password: str
    
class CustomerLogin(BaseModel):
    pass
    
class CustomerCreate(CustomerBase):
    name: str
    last_name: str
    address: str
    zip_code: str
    is_active: bool = True
    company: str
    


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# Signup

class SignUpSchema(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

class SignInSchema(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Item

class ItemBase(BaseModel):
    name: str
    is_active: bool = True
    description: str
    category: str
    price: float
    stock: int = 1
    daily_rate: float = 20.5
    
class ItemCreate(ItemBase):
    proportions: str
    model: str 
    images: str
    availability: bool
    type: str
    manufacturer: str

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True



# TransactionProduct schema
class TransactionProductBase(BaseModel):
    item_id: int
    quantity: int

class TransactionProductCreate(TransactionProductBase):
    pass

class TransactionProductResponse(TransactionProductBase):
    id: int

    class Config:
        orm_mode = True


# Transaction schema
class TransactionBase(BaseModel):
    # id: int
    rental_start_date: datetime
    rental_end_date: datetime
    total_price: float
    status: Optional[str] = "Pending"

class TransactionCreate(TransactionBase):
    products: List[TransactionProductCreate]  # List of products and quantities

class TransactionResponse(TransactionBase):
    transaction_id: int
    products: List[TransactionProductResponse]

    class Config:
        orm_mode = True