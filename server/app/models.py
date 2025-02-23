from django.db import models
from config.dbConfig import *
# Create your models here.

user_collection = db['User']
class_collection = db['Class']
roles_collection = db['Roles']
