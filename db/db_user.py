from sqlalchemy.orm.session import Session
from schemas.user_schema import UserBase
from db.models import User
from db.hash import Hash
from fastapi import HTTPException,status


#Create user  db_user file altindakiler controllers user controllers
def create_user(db:Session,request:UserBase):
    new_user=User(
        firstname=request.firstname,
        lastname=request.lastname,
        email=request.email,
        hashed_password=Hash.bcrypt(request.hashed_password)
        
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db:Session):
    user_list=db.query(User).all()
    if not user_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user found")

    return user_list

#read user
def get_one_user(db:Session,id:int):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    return user

