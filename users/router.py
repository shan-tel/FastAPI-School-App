from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from . import models, schemas
from .utils import hash_password
from authentication.oauth2 import get_current_user

router = APIRouter(prefix = "/users", tags =["Users"])

@router.post("/register", response_model = schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code = 400, detail = "Email already registered")

    new_user = models.User(
    username = user_data.username,
    email = user_data.email,
    full_name = user_data.full_name,
    hashed_password = hash_password(user_data.password),
    role = user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model = list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    requesting_user = db.query(models.User).filter(models.User.id == current_user_id).first()
    
    if requesting_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view all users")
        
    return db.query(models.User).all()

@router.get("/{user_id}", response_model= schemas.UserResponse)
def get_user(user_id: int, db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    return user

@router.put("/{user_id}", response_model= schemas.UserResponse)
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session= Depends(get_db), current_user_id: int = Depends(get_current_user)):
    requesting_user = db.query(models.User).filter(models.User.id == current_user_id).first()
    
    if requesting_user.id != user_id and requesting_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this account")
    user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(status_code= 404, detail= "User not found")

    update_data = updated_user.model_dump(exclude_unset=True, exclude_none=True)

    user_query.update(update_data, synchronize_session= False)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    requesting_user = db.query(models.User).filter(models.User.id == current_user_id).first()
    
    if requesting_user.id != user_id and requesting_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this account")
    user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(status_code= 404, detail= "User not found")

    user_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"User {user_id} deleted successfully"}
    

