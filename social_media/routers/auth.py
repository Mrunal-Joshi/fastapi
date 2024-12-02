from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..database import get_db
from ..schemas import UserLogin
from ..models import User
from sqlalchemy.orm import Session
from ..utils import verify

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(credentials : UserLogin, db : Session = Depends(get_db)):
    db_credentials = db.query(User).filter(User.email==credentials.email).first()
    if not db_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    else:
        if verify(credentials.password, db_credentials.password):
            return "Authorised User"
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail = "UNAUTHORIZED USER")