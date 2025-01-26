from fastapi import APIRouter, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import get_user
from models import UserInput, UserOutput, TokenOutput
from key_tool import create_access_token, decode_access_token, hash_password


security = HTTPBearer()
router = APIRouter(prefix="/api/v1/authentication", tags=["Authentication"])


@router.post("/token", response_model=TokenOutput)
async def login_for_access_token(user_data: UserInput):
    user = get_user(user_data.email)
    if not user or user["password"] != hash_password(user_data.password.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/decode_token")
async def decode_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    return {"message": "Token is valid", "payload": payload}


@router.get("/me", response_model=UserOutput)
async def read_users_me(credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    payload = decode_access_token(access_token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload["sub"]
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return UserOutput(**user)
