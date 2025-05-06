from fastapi import FastAPI

from performer.routers.v1 import hello, routers_users

app = FastAPI()


app.include_router(hello.router)
app.include_router(routers_users.router)
