from  pydantic import BaseModel

class UserBase(BaseModel):
    firstname:str
    lastname:str
    email:str
    hashed_password:str

class UserDisplay(BaseModel):
    firstname:str
    lastname:str
    email:str
    class Config():
        orm_mode=True
    