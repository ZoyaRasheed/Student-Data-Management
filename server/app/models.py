from django.db import models
from config.db import *
# Create your models here.

user_collection = db['User']
class_collection = db['Class']
roles_collection = db['Roles']
mark_collection = db['Marks']