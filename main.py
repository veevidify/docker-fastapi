from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

# some configs - would be stored in config file
# openssl rand -hex 32 # to sign jwt
SECRET = "8cec9983c4fdafe4c6f1bedbab9531b063e32fc31cda7e9f93715e951cebcd3a"
ALG = "HS256"
ACCESS_TOKEN_EXPIRES = 3600

app = FastAPI()

# In [3]: pwdctx.hash("123456")
# Out[3]: '$2b$12$pThsfCavxZ84aSzRXjdAhOk.lTSq2jlV5h8sLSTxDNdOpIW6Ljt4G'
users = {
    "ve1": {
        "username": "ve1",
        "full_name": "V N",
        "email": "v1@gmail.com",
        "hashed_password": "$2b$12$pThsfCavxZ84aSzRXjdAhOk.lTSq2jlV5h8sLSTxDNdOpIW6Ljt4G",
        "disabled": False
    },
    "ve2": {
        "username": "ve2",
        "full_name": "V N",
        "email": "v2@gmail.com",
        "hashed_password": "$2b$12$pThsfCavxZ84aSzRXjdAhOk.lTSq2jlV5h8sLSTxDNdOpIW6Ljt4G",
        "disabled": True
    }
}

# authenticatable models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserDB(User):
    hashed_password: str

# encryption algo enabled
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_pw(plaintext: str):
    return pwd_context.hash(plaintext)

def verify_hash(plaintext: str, hashed: str):
    return pwd_context.verify(plaintext, hashed)

# simulating read db/ collection/ storage
def retrieve_user(users_coll, username: str):
    if (username in users_coll):
        user_dict = users_coll[username]

        return UserDB(**user_dict)
    return None

def authenticate_user(users_coll, username: str, password: str):
    user = retrieve_user(users_coll, username)
    if (not user):
        return False
    elif (not verify_hash(password, user.hashed_password)):
        return False

    return user

def create_access_token(data: dict, expires_after: Optional[timedelta] = None):
    payload = data.copy()
    if (expires_after):
        expires = datetime.utcnow() + expires_after

    else:
        expires = datetime.utcnow() + timedelta(seconds=3600)

    payload.update({"exp": expires})
    encoded_jwt = jwt.encode(payload, SECRET, algorithm=ALG)

    return encoded_jwt

# get current user from token dependency
# injectable & reusable every route
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    invalid_creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    inactive_user_exc = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Inactive user."
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALG])
        username: str = payload.get("sub")
        if (username is None):
            raise invalid_creds_exc
        token_data = TokenData(username=username)
    except JWTError:
        raise invalid_creds_exc

    user = retrieve_user(users, username)

    if (not user):
        raise invalid_creds_exc

    if (not user or user.disabled):
        raise inactive_user_exc

    return User(**user.dict())

# token login route for oauth2 package to use to exchange for token
@app.post("/token")
async def login_exchange_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    wrong_login_info_exc = HTTPException(
        status_code=400,
        detail="Incorrect username or password."
    )

    user = authenticate_user(users, form_data.username, form_data.password)
    if (not user):
        raise wrong_login_info_exc

    token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_after=token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# example to inject current user retrieval from token
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user
