from django.db import models
from models import User

# Create your models here.
class Lk(models.Model):
	user_name = models.ForeginKey(User, on_delete = models.CASCADE)
    bot = models.CharField('bot_id', max_length = 50)

	# def __str__(self):
	# 	return self.user_name

	# class Meta:
	# 	verbose_name = ""
