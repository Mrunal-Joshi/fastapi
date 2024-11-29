from passlib.context import CryptContext
# set default hashing algo to bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)