from http import HTTPStatus

from fastapi import FastAPI

from performer.routers.v1 import routers_users

app = FastAPI()


@app.get('/')
def hello():
    return {
        'message': 'Ola, bem-vindo ao Performer!'
        ' Para acessar a API, use /docs ou /redoc'
    }


@app.get('/health', status_code=HTTPStatus.OK)
def health():
    return {'status': 'ok'}


app.include_router(routers_users.router)
