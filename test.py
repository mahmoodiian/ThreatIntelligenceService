from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

# Secret key to sign the JWT token
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Function to create a JWT token
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode a JWT token
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake user model (Replace this with your user model)
class User:
    def __init__(self, username: str):
        self.username = username

# Function to authenticate users
def authenticate_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Replace this with your user retrieval logic
    user = User(username=username)
    if user is None:
        raise credentials_exception
    return user

# Endpoint to get token (authenticate)
@app.post("/token")
async def login_for_access_token(form_data: dict):
    # Replace this with your authentication logic
    username = form_data["username"]
    password = form_data["password"]

    # Replace this with your actual user authentication logic
    # For example, you might check the username and password against a database
    # For simplicity, this example assumes a hardcoded username and password
    correct_username = "example_user"
    correct_password = "example_password"
    if username == correct_username and password == correct_password:
        # Create a token with an expiration time (15 minutes in this example)
        token_expires = timedelta(minutes=15)
        token = create_jwt_token({"sub": username}, expires_delta=token_expires)
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected endpoint that requires authentication
@app.get("/protected")
async def protected_route(current_user: User = Depends(authenticate_user)):
    return {"message": "This is a protected endpoint", "username": current_user.username}