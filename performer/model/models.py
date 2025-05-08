from sqlalchemy.orm import registry

table_registry = registry()

from .nutrition_model import *
from .socia_models import *
from .user_models import *
from .workout_models import *
