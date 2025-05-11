from fastapi import FastAPI

from performer.routers.v1.nutrition import (
    routers_food_items,
    routers_user_meal_logs,
)
from performer.routers.v1.social import (
    routers_achievements,
    routers_social_comments,
    routers_social_likes,
    routers_social_posts,
    routers_user_achievements,
)
from performer.routers.v1.users import (
    hello,
    routers_progress_tracking,
    routers_user_exercise_logs,
    routers_user_workout_schedules,
    routers_user_workout_sessions,
    routers_users,
    routers_users_details,
)
from performer.routers.v1.workout import (
    routers_cardio_exercises,
    routers_equipment,
    routers_exercises,
    routers_user_cardio_logs,
    routers_user_hiit_logs,
    routers_workout,
    routers_workout_exercises,
)
from performer.tools.tool_logs import lifespan


description = """
A API Performer permite aos usuários melhorar sua jornada fitness. 🚀

## Verificação de Saúde

* **Verificar a saúde do sistema**.

## Usuários

Você pode:

* **Criar usuários**.
* **Consultar detalhes dos usuários**.
* **Acompanhar progresso**.
* **Gerenciar agendas de treino**.
* **Registrar exercícios**.

## Treino

Você pode:

* **Gerenciar sessões de treino**.
* **Explorar exercícios**.
* **Acompanhar registros de cardio e HIIT**.
* **Gerenciar equipamentos de treino**.

## Social

Você pode:

* **Publicar conquistas**.
* **Curtir e comentar em publicações**.
* **Acompanhar conquistas de usuários**.

## Nutrição

Você pode:

* **Registrar refeições**.
* **Explorar itens alimentares**.
"""


app = FastAPI(lifespan=lifespan,version='0.0.1',
               summary="Performer API", 
               description=description,
               title="Performer API")    

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
