from fastapi import FastAPI
from handlers import router as auth_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the authentication router which contains routes for user authentication
app.include_router(auth_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Authentication API is running!"}
