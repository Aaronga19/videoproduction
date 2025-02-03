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



router = APIRouter(
    prefix="/users",
    tags=['Users']
)
TOKEN_EXPIRATION = 10

@router.post("/create", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: db_dependency):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db, user=user)
    return Response(f"{user.username} was created successfully",status_code=status.HTTP_201_CREATED)


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

@router.get("/me")
async def read_users_me(
    current_user: Annotated[schemas.UserResponse, Depends(auth.get_current_active_user)],
):

    return current_user