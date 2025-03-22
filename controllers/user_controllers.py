from sqlalchemy.orm.session import Session
from schemas.user_schema import UserBase
from db.models import User
from db.hash import Hash
from fastapi import HTTPException,status
import logging
from sqlalchemy.exc import IntegrityError


#Create user  
def create_user(db:Session,request:UserBase):
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session object used to interact with the database.
        request (UserBase): The request object containing user details (firstname, lastname, email, hashed_password).

    Returns:
        User: The newly created user object.

     Raises:
        ValueError: If the email is invalid or the user already exists.    


    """
    new_user=User(
        firstname=request.firstname,
        lastname=request.lastname,
        email=request.email,
        hashed_password=Hash.bcrypt(request.hashed_password)
        
    )
    try:
        # Add and commit the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        # Rollback the transaction in case of error
        db.rollback()
        logging.error(f"User with email {request.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")

    # Log successful creation
    logging.info(f"User {request.email} created successfully")

    return new_user


#read user
def get_one_user(db:Session,id:int):
    """
    Retrieve a single user by their ID.

    Args:
        id (int): The ID of the user to retrieve.
        db (Session): The database session object.

    Returns:
        UserDisplay: The user object if found.

    Raises:
        HTTPException: If the user with the specified ID is not found."
        """
    try:

        user=db.query(User).filter(User.id==id).first()
        if not user:
            # Log the error and raise an HTTPException if the user is not found
            logging.error(f"User with ID {id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {id} not found"
            )
    except Exception as e:
        # Log the error and raise an HTTPException if something goes wrong
        logging.error(f"Error retrieving user with ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the user"
        )

    # Log successful retrieval
    logging.info(f"User with ID {id} retrieved successfully")

    return user

#update  user 
def update_user(db:Session,id:int,request:UserBase):
    """
    Update a user's details in the database.

    Args:
        db (Session): The database session object.
        id (int): The ID of the user to update.
        request (UserBase): The request object containing updated user details.

    Returns:
        dict: A dictionary containing the updated user's details.

    Raises:
        HTTPException: If the user is not found, the email is invalid, or a database error occurs.
    """
    user = db.query(User).filter(User.id == id).first()
      #handle any exceptions
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    try:
        user.firstname = request.firstname
        user.lastname = request.lastname
        user.email = request.email
        user.hashed_password = Hash.bcrypt(request.hashed_password)

        db.commit()
        db.refresh(user) 
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        logging.error(f"Error updating user with ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user"
        )    
    return f"User {user.firstname} {user.lastname} (ID: {user.id}) has been updated."

#  delete user 
def delete_user(db:Session,id:int):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        logging.error(f"Error deleting user with ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user"
        )
    
        
    return f"User {user.firstname} {user.lastname} (ID: {user.id}) has been deleted."