from fastapi import FastAPI

from performer.routers.v1.users import (
    hello,
    routers_user_workout_sessions,
    routers_users,
    routers_users_details,
)
from performer.routers.v1.workout import routers_workout
from performer.tools.tool_logs import lifespan

app = FastAPI(lifespan=lifespan)


app.include_router(hello.router)
app.include_router(routers_users.router)
app.include_router(routers_users_details.router)
app.include_router(routers_workout.router)
app.include_router(routers_user_workout_sessions.router)
