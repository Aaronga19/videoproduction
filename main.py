from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Create an instance of Jinja2Templates and point it to the templates directory
templates = Jinja2Templates(directory="templates")

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