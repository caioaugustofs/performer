
# Performer

Performer é um aplicativo desenvolvido para promover o alto rendimento em exercícios físicos. O objetivo do projeto é fornecer ferramentas, acompanhamento e recursos que auxiliem atletas e entusiastas a melhorarem sua performance, monitorando treinos, progresso e oferecendo recomendações personalizadas.

## Principais funcionalidades
- Registro e acompanhamento de treinos
- Monitoramento de desempenho
- Análise de progresso
- Recomendações personalizadas para evolução

O Performer visa ser uma solução completa para quem busca excelência e resultados em atividades físicas.
## Estrutura de dados

```
users ──┐  
        ├─ user_details  
        ├─ user_workout_sessions ── user_exercise_logs  
        ├─ user_workout_schedules  
        ├─ progress_tracking  
        ├─ user_meal_logs  
        ├─ social_posts ── social_comments  
        │                └─ social_likes  
        ├─ subscriptions  
        └─ messages  

workouts ── workout_exercises ── exercises ── exercise_equipment ── equipment
```
