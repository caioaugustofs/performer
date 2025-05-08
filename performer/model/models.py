from sqlalchemy.orm import registry

table_registry = registry()

from .user_models import *
from .workout_models import *