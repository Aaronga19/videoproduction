from fastapi import FastAPI, status
from routers import users
app = FastAPI(
    title='Users Microservice',
    description='This microservice manage the users and their activity',
    version='1.0'
)

origins = ["*"]


app.get('/users/', status_code= status.HTTP_200_OK)
def register_user():
    return {'message': 'User information'}



origins = ["*"]

# ROUTERS
app.include_router(users.router)
# app.include_router(duplicated.router)
    
@app.get("/", status_code=status.HTTP_200_OK) 
async def get_user(): 
    return {"message": "Welcome to Users-Marvel-Store"}