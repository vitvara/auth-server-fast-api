from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



auth_handler = AuthHandler()
users = []

@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        print(auth_details.username)
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    if len(users) == 0:
        permission = 1
    else:
        permission = 0
    users.append({
        'username': auth_details.username,
        'password': hashed_password,
        'permission':permission    
    })
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/getpermission')
def protected(username=Depends(auth_handler.auth_wrapper)):
    permission = None
    for x in users:
        if x['username'] == username:
            permission = x['permission']
            break
    if permission == 1:
        return {'name': username}
    else:
        raise HTTPException(status_code=401, detail='Permission denined')