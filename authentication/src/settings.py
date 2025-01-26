import os
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from a .env file
load_dotenv()


# Algorithm and secret key used for encoding and decoding JWT tokens
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
JWT_SECRET_PATH = os.getenv("JWT_SECRET_PATH")

# The expiration time for access tokens in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10))

# The directory where to store the data
DATA_DIRECTORY_PATH = os.getenv("DATA_DIRECTORY_PATH", "data")

# Use the content of the file specified in JWT_SECRET_PATH as the secret key if the file exists
if JWT_SECRET_PATH:
    JWT_SECRET_KEY = Path(JWT_SECRET_PATH).read_text() if Path(JWT_SECRET_PATH).exists() else JWT_SECRET_KEY
