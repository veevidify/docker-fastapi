from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

users = {
    "ve1": {
        "username": "ve1",
        "full_name": "V N",
        "email": "v1@gmail.com",
        "hashed_password": "mockhashed_1",
        "disabled": False
    },
    "ve2": {
        "username": "ve2",
        "full_name": "V N",
        "email": "v2@gmail.com",
        "hashed_password": "mockhashed_2",
        "disabled": True
    }
}

def mock_hash_password(plaintext: str):
    return "mockhashed_" + plaintext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserDB(User):
    hashed_password: str

def retrieve_user(coll, username: str):
    if (username in coll):
        user_dict = coll[username]

        return UserDB(**user_dict)
    return None

def mock_decode_token(token):
    user = retrieve_user(users, token)
    return user

# get current user from token dependency
# injectable & reusable every route
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    user = mock_decode_token(token)

    if (not user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    elif (user.disabled):
        raise HTTPException(status_code=400, detail="Inactive user.")

    return user

# token login route for oauth2 package to use to exchange for token
@app.post("/token")
async def token_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users.get(form_data.username)
    if (not user_dict):
        raise HTTPException(status_code=400, detail="Incorrect username or password.")
    user = UserDB(**user_dict)
    hashed_password = mock_hash_password(form_data.password)
    if (not hashed_password == user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password.")

    return {"access_token": user.username, "token_type": "bearer"}

# inject current user retrieval from token
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user

