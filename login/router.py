from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from users import models
from users.utils import verify_password
from authentication.oauth2 import create_access_token  
from . import schemas
import jwt
from authentication.oauth2 import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM



router = APIRouter(tags=["Login"])

@router.post("/login", response_model=schemas.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
        
    
    token_payload = {"user_id": user.id, "role": user.role}
    real_token = create_access_token(data=token_payload)
    refresh_token = create_refresh_token(data=token_payload)
    
    return {
        "access_token": real_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@router.post("/refresh")
def refresh_access_token(request: schemas.TokenRefreshRequest):
    
    payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    role = payload.get("role")

    new_access_token = create_access_token(data={"user_id": user_id, "role": role})
    return {"access_token": new_access_token, "token_type": "bearer"}