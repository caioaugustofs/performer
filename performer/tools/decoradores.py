from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from performer.tools.tool_logs import logger

"""
Decorador para commit, refresh e retorno de objetos em funções.
assíncronas que usam SQLAlchemy AsyncSession.
Uso:
    @commit_and_refresh()
    async def func(..., session, ...):
        ...
        session.add(obj)
        return obj

    Ou personalizado:
    @commit_and_refresh(status_code=400, detail="Erro ao atualizar usuário")
    async def func(...):
        ...
"""


def commit_and_refresh(
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    detail='Erro ao processar a operação.',
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Procura o argumento 'session' (AsyncSession)
            session = kwargs.get('session')
            if session is None:
                # tenta encontrar por posição
                for arg in args:
                    if isinstance(arg, AsyncSession):
                        session = arg
                        break
            if session is None:
                raise ValueError(
                    'AsyncSession não encontrado nos argumentos da função '
                    'decorada.'
                )

            try:
                obj = await func(*args, **kwargs)
                await session.commit()
                await session.refresh(obj)
                logger.info(
                    'Operação realizada com sucesso.',
                )
                return obj
            except Exception:
                await session.rollback()
                logger.error(
                    'Erro ao processar a operação.',
                    exc_info=True,
                )
                raise HTTPException(
                    status_code=status_code,
                    detail=detail,
                )

        return wrapper

    return decorator
