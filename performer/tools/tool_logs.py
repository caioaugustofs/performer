import logging
from contextlib import asynccontextmanager

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app):
    logger.info('Iniciando api Performer')
    yield
    logger.info('Finalizando api Performer')
