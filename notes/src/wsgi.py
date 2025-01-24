from fastapi import FastAPI
from handlers import router as note_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the note router which contains routes for interacting with the notes
app.include_router(note_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Note API is running!"}
