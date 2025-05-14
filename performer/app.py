from fastapi import FastAPI

from performer.routers.v1.users import (
    hello,
    routers_user_workout_sessions,
    routers_users,
    routers_users_details,
)
from performer.routers.v1.workout import (
    routers_equipment,
    routers_exercises,
    routers_workout,
)
from performer.tools.tool_logs import lifespan

description = """
The Performer API helps users enhance their fitness journey. 🚀
It provides endpoints for managing workouts, tracking progress, and
connecting with a community of fitness enthusiasts. 💪
"""


app = FastAPI(
    lifespan=lifespan,
    version='0.0.1',
    description=description,
    title='Performer API',
)


# ------------------- Health Check -------------------
app.include_router(hello.router)
# ------------------- Users -------------------'
app.include_router(routers_users.router)
app.include_router(routers_users_details.router)
# app.include_router(routers_progress_tracking.router)
# app.include_router(routers_user_workout_schedules.router)
# app.include_router(routers_user_exercise_logs.router)
# ------------------- Workout -------------------
app.include_router(routers_user_workout_sessions.router)
app.include_router(routers_workout.router)
app.include_router(routers_equipment.router)
app.include_router(routers_exercises.router)
# app.include_router(routers_workout_exercises.router)
# app.include_router(routers_user_hiit_logs.router)
# app.include_router(routers_cardio_exercises.router)
# app.include_router(routers_user_cardio_logs.router)
# ------------------- Social -------------------
# app.include_router(routers_achievements.router)
# app.include_router(routers_user_achievements.router)
# app.include_router(routers_social_posts.router)
# app.include_router(routers_social_comments.router)
# app.include_router(routers_social_likes.router)
# ------------------- Nutrition -------------------
# app.include_router(routers_food_items.router)
# app.include_router(routers_user_meal_logs.router)
