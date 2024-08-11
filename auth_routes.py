from database import session, engine
from fastapi import APIRouter, status, HTTPException, Depends
from models import Users
from schemas import UserRegister, User, UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from sqlalchemy import or_
from fastapi_jwt_auth import AuthJWT
import datetime
from fastapi.encoders import jsonable_encoder


session = session(bind=engine)
auth_router = APIRouter(
    prefix='/auth'
)

logging.basicConfig(level=logging.INFO)
@auth_router.post("/register", status_code=201)
async def register(user: UserRegister):
    db_email = session.query(Users).filter(Users.email == user.email).first()
    if db_email is not None:
        return {"message": "Email already exists", "status_code": status.HTTP_400_BAD_REQUEST}
    db_username = session.query(Users).filter(Users.username == user.username).first()
    if db_username is not None:
        return {"message": "Username already exists", "status_code": status.HTTP_400_BAD_REQUEST}
    new_user = Users(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        telephone_number=user.telephone_number,
        region=user.region,
        is_admin=user.is_admin,
        is_verified=user.is_verified
    )

    session.add(new_user)
    session.commit()
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "telephone_number": user.telephone_number,
        "region": user.region,
        "is_admin": user.is_admin,
        "is_verified": user.is_verified
    }
    return {
        "message": "User created successfully",
        "new_user": user_data,
        "status_code": status.HTTP_201_CREATED
    }

@auth_router.post("login/", status_code=200)
async def login(user: UserLogin, Authorize: AuthJWT=Depends()):

    db_user = session.query(Users).filter(
        or_(
            Users.username == user.username_or_email,
            Users.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=20)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        response_data = {
            "message": "Successfully logged in",
            "status": status.HTTP_200_OK,
            "token": token
        }
        return response_data
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username/email or password!")


@auth_router.get("/login/refresh", status_code=200)
async def refresh_token(Authorize: AuthJWT=Depends()):

    try:
        refresh_lifetime = datetime.timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(Users).filter(Users.username == current_user).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

        new_refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)
        response_model = {
            "Success": True,
            "refresh_token": new_refresh_token
        }
        return jsonable_encoder(response_model)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


