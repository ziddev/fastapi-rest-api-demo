from fastapi import FastAPI
from handlers import router as money_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the money router which contains routes for interacting with the currencies
app.include_router(money_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Money API is running!"}
