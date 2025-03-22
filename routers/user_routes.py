from fastapi import APIRouter,Depends
from schemas.user_schema import UserBase,UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import user_controllers
from typing import List

router=APIRouter(
    prefix='/user',
    tags=['user']
)

#Create user
@router.post('/',response_model=UserDisplay)
def create_user(request:UserBase,db:Session=Depends(get_db)):
    return user_controllers.create_user(db,request)



#Read one User
@router.get('/{id}',response_model=UserDisplay)
def get_one_user(id:int,db:Session=Depends(get_db)):
    return user_controllers.get_one_user(db,id)

#Update User
@router.post('/{id}/update')
def update_user(id:int,request:UserBase,db:Session=Depends(get_db)):
    return user_controllers.update_user(db,id,request)
 
 #Delete User
@router.get('/{id}/delete')
def delete_user(id:int,db:Session=Depends(get_db)):
    return user_controllers.delete_user(db,id)

