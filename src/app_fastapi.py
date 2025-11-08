from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database import get_db
from src import models
from src.utils.hashing import hash_password, verify_password
from src.utils.jwt import create_access_token, verify_token
from src.utils.schemas import UserCreate, UserLogin, UserRead
from datetime import timedelta
import uvicorn

app = FastAPI()

# OAuth2PasswordBearer는, swagger UI의 Authorize 버튼과 연동됨
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/login/')

@app.post('/users/', response_model = UserRead)
def create_user(user: UserCreate,
                db: Session = Depends(get_db)):
    db_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/login/')
def login(username: str = Form(...),
          password: str = Form(...),
          db: Session = Depends(get_db)):
    # Form 데이터 -> pydantic 모델로 변환
    user_data = UserLogin(username = username,
                          password = password)

    db_user = db.query(models.User).filter(models.User.name == user_data.username).first()
    if not db_user or not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code = 400, detail = "해당 사용자가 없습니다")
    
    # JWT token 생성
    access_token_expires = timedelta(minutes = 30)
    access_token = create_access_token(
        data = {"sub": db_user.name},               # payload에 사용자 식별자 넣기
        expires_delta = access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}



@app.get('/users/me', response_model = UserRead)
def read_users_me(token: str = Depends(oauth2_scheme),
                  db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code = 401, detail = '확인되지 않은 token입니다')
    
    username = payload.get('sub')
    if username is None:
        raise HTTPException(status_code = 401, detail = '확인되지 않은 token payload입니다')
    
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        raise HTTPException(status_code = 401, detail = '유저를 찾을 수 없습니다')
    
    return user

# users = []

# @app.get('/ping-db')
# def ping_db(db: Session = Depends(get_db)):
#     result = db.execute(text("SELECT 1")).scalar()
#     return {"db": "ok" if result == 1 else "fail"}

# @app.get('/hello/{name}')
# def say_hello(name: str):
#     return {'message': f"안녕, {name}!"}

# @app.get('/items/')
# def get_item(skip: int = 0,
#              limit: int = 10):
#     return {'skip': skip, 'limit': limit}

# @app.post('/items/')
# def create_item(item: Item):
#     return {'message': '아이템 생성됨', 'item': item}

# @app.get('/users')
# def get_users():
#     return users 

# @app.post('/users')
# def create_user(user: User):
#     users.append(user)
#     return {'message': 'User 생성완료', 'user': user}

# @app.get('/users/{user_name}')
# def get_user(user_name: str):
#     for user in users:
#         if user.name == user_name:
#             # password 빼고 반환
#             return {'message': 'User 찾음', 'user': {'name': user.name, 'email': user.email}}
#     return HTTPException(status_code=404, detail='사용자가 없습니다.')

# @app.put('/users/{user_name}')
# def change_user_info(user_name: str,
#                      new_user: User):
#     for user in users:
#         if user.name == user_name:
#             users.append(user)
#             return user

if __name__ == '__main__':
    uvicorn.run(
        app,
        host = 'localhost',
        port = 8000,
        reload = True
    )