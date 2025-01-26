from fastapi import FastAPI
from handlers import router as task_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the task router which contains routes for interacting with the tasks
app.include_router(task_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Task API is running!"}
