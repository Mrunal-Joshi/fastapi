from passlib.context import CryptContext
# set default hashing algo to bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(password : str, hashed_password):
    return pwd_context.verify(password, hashed_password)