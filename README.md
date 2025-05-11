# Performer

Performer é um aplicativo desenvolvido para promover o alto rendimento em exercícios físicos. O objetivo do projeto é fornecer ferramentas, acompanhamento e recursos que auxiliem atletas e entusiastas a melhorarem sua performance, monitorando treinos, progresso e oferecendo recomendações personalizadas.

## Principais Funcionalidades

- **Registro e acompanhamento de treinos**
- **Monitoramento de desempenho**
- **Análise de progresso**
- **Recomendações personalizadas para evolução**

O Performer visa ser uma solução completa para quem busca excelência e resultados em atividades físicas.

## Estrutura de Dados

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

## API Performer

A API Performer permite aos usuários melhorar sua jornada fitness. 🚀

### Verificação de Saúde

- **Verificar a saúde do sistema**.

### Usuários

A API permite:

- **Criar usuários**.
- **Consultar detalhes dos usuários**.
- **Acompanhar progresso**.
- **Gerenciar agendas de treino**.
- **Registrar exercícios**.

### Treino

A API permite:

- **Gerenciar sessões de treino**.
- **Explorar exercícios**.
- **Acompanhar registros de cardio e HIIT**.
- **Gerenciar equipamentos de treino**.

### Social

A API permite:

- **Publicar conquistas**.
- **Curtir e comentar em publicações**.
- **Acompanhar conquistas de usuários**.

### Nutrição

A API permite:

- **Registrar refeições**.
- **Explorar itens alimentares**.
