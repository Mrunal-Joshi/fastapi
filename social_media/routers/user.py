from fastapi import status, Depends
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter

router = APIRouter(prefix="/users")


#USER APIS
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # hash the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.DisplayUser)
def get_user(id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User does not exit")
    return user
