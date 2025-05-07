from fastapi import FastAPI

from performer.routers.v1 import hello, routers_users, routers_users_details

app = FastAPI()


app.include_router(hello.router)
app.include_router(routers_users.router)
app.include_router(routers_users_details.router)
