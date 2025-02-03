from fastapi.routing import APIRouter
from typing import Annotated
from datetime import timedelta
from fastapi import Request, HTTPException, status, Depends 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import crud, auth
from database import schemas
from database.database import db_dependency
from jose import  JWTError
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/customers",
    tags=['Customer']
)

SECRET_KEY = "f188743c49229ac65f52a76585f613d07ae026ba0e3eb74992457f2e8a00110e"
TOKEN_EXPIRATION = 10
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")
# user_dependency = Annotated[dict, Depends(auth.get_current_user)]





@router.post("/logout", response_class=HTMLResponse)
def logout(request: Request):
    return RedirectResponse("/customers/login", 
                            status_code=status.HTTP_302_FOUND, 
                            headers={"set-cookie": "access_token=; Max-Age=0"}
                            )
    
# Create
@router.post("/signup", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: schemas.CustomerCreate, db: db_dependency):
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(
            status_code=400, detail="Email already registered")
    crud.create_customer(db, customer=customer)
    return RedirectResponse("/customers/login", status_code=status.HTTP_201_CREATED)


# Read
@router.get("/me")
async def read_users_me(
    current_user: Annotated[schemas.CustomerResponse, Depends(auth.get_current_active_user)],
):
    del current_user.password

    return current_user

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request:Request, current_user: Annotated[dict, Depends(auth.get_current_active_user)]):
    if current_user is None:                                                                                
        return RedirectResponse("/customers/login", status_code=status.HTTP_302_FOUND)
    try:
        return templates.TemplateResponse("customers/dashboard.html", {
        "request":request,
        "title": "Dashboard",
        "message": "Dashboard",
        "username": current_user.name
    })  
    except JWTError:
        return RedirectResponse("/customers/login", status_code=status.HTTP_403_FORBIDDEN)

@router.get("/customer/{id}")
async def get_customer_by_id(id: int, db: db_dependency):
    customer = crud.get_customer_by_id(db,id)
    return customer 

@router.delete("/account/delete")
def delete_account(request:Request, current_user: Annotated[dict, Depends(auth.get_current_active_user)], db: db_dependency):
    print("curren user", current_user.email)
    response = crud.delete_customer(db,current_user.email)
    print(response)
    return {"message": f"your account {current_user.email} was deleted successfully"}

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token( db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.authenticate_customer(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRATION)
    access_token = auth.create_access_token(
        data={"sub": f"{user.email}"}, expires_delta=access_token_expires
    )
    return dict(access_token=access_token, token_type="bearer")
