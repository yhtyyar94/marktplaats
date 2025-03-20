from fastapi import APIRouter,Depends
from schemas.user_schema import UserBase,UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List

router=APIRouter(
    prefix='/user',
    tags=['user']
)

#Create user
@router.post('/',response_model=UserDisplay)
def create_user(request:UserBase,db:Session=Depends(get_db)):
    return db_user.create_user(db,request)

#Read all User
@router.get('/',response_model=List[UserDisplay])
def get_all_users(db:Session=Depends(get_db)):
    return db_user.get_all_users(db)

#Read one User
@router.get('/{id}',response_model=UserDisplay)
def get_one_user(id:int,db:Session=Depends(get_db)):
    return db_user.get_one_user(db,id)

