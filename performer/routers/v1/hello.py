from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(tags=['Hello'])


@router.get('/')
def hello():
    return {
        'message': 'Ola, bem-vindo ao Performer! '
        'Para acessar a documentação da API, use /docs ou /redoc'
    }


@router.get('/health', status_code=HTTPStatus.OK)
def health():
    return {'status': 'ok'}
