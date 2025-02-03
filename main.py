from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import models
from database.database import engine, SessionLocal, Base, db_dependency
from routers import users, customers, inventory, test, transactions
import time

app = FastAPI()
# Create an instance of Jinja2Templates and point it to the templates directory
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(customers.router)
app.include_router(transactions.router)
# app.include_router(test.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time)
    message = "huevos"
    print(f"middleware: \t{message}") 
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the index.html template and pass data to it
    return templates.TemplateResponse("home/index.html", {"request": request, "title": "AAF", "message": "Welcome to VideoProducer"})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("info/about.html", {
        "request": request,
        "title": "About Us",
        "message": "This is the about page of our FastAPI app."
    })

@app.get("/contract", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("users/contract.html", {
        "request": request,
        "title": "Contract",
        "message": "This is the contract to rent"
    })