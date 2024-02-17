from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake user model for demonstration purposes
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

# Fake user data
fake_users_db = {
    "testuser": User(username="testuser", password="password123")
}

# OAuth2PasswordBearer is used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    return username


# Route to get a token
@app.post("/token")
async def login(form_data: dict):
    username = form_data["username"]
    password = form_data["password"]

    user = fake_users_db.get(username)
    if user is None or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route that requires a valid token
@app.get("/protected")
async def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Hello {username}, you are in a protected route!"}
#
# if __name__ == "__main__":
#     app()
