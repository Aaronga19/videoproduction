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
    prefix="/inventory",
    tags=['Inventory']
)


@router.post("/create", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(item: schemas.ItemCreate, db: db_dependency):
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(
            status_code=400, detail="Item already registered")
    crud.create_item(db, item=item)
    return Response(f"{item.name} was created successfully", status_code=status.HTTP_201_CREATED)