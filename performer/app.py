from fastapi import FastAPI

from performer.routers.v1.users import (
    hello,
    routers_user_workout_sessions,
    routers_users,
    routers_users_details,
    routers_progress_tracking,
    routers_user_workout_schedules,
    routers_user_exercise_logs,
)
from performer.routers.v1.workout import (
    routers_workout,
    routers_exercises,
    routers_workout_exercises,
    routers_equipment,
    routers_user_hiit_logs,
    routers_cardio_exercises,
    routers_user_cardio_logs,
)
from performer.routers.v1.nutrition import (
    routers_food_items,
    routers_user_meal_logs,
)
from performer.routers.v1.social import (
    routers_achievements,
    routers_user_achievements,
    routers_social_posts,
    routers_social_comments,
    routers_social_likes,
)
from performer.tools.tool_logs import lifespan

app = FastAPI(lifespan=lifespan)

# ------------------- Health Check -------------------
app.include_router(hello.router)
# ------------------- Users -------------------'
app.include_router(routers_users.router)
app.include_router(routers_users_details.router)
app.include_router(routers_progress_tracking.router)
app.include_router(routers_user_workout_schedules.router)
app.include_router(routers_user_exercise_logs.router)
# ------------------- Workout -------------------
app.include_router(routers_user_workout_sessions.router)
app.include_router(routers_workout.router)
app.include_router(routers_exercises.router)
app.include_router(routers_workout_exercises.router)
app.include_router(routers_equipment.router)
app.include_router(routers_user_hiit_logs.router)
app.include_router(routers_cardio_exercises.router)
app.include_router(routers_user_cardio_logs.router)
# ------------------- Social -------------------
app.include_router(routers_achievements.router)
app.include_router(routers_user_achievements.router)
app.include_router(routers_social_posts.router)
app.include_router(routers_social_comments.router)
app.include_router(routers_social_likes.router)
# ------------------- Nutrition -------------------
app.include_router(routers_food_items.router)
app.include_router(routers_user_meal_logs.router)

