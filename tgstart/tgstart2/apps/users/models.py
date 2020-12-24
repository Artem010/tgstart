from django.db import models


class User(models.Model):
	user_name = models.CharField('Логин', max_length = 30)
	user_firstname = models.TextField('Имя', max_length = 30)
	user_lastname = models.TextField('Фамилия', max_length = 30)
	id_user = models.CharField('id_user', max_length = 10)
	user_email = models.CharField('Email', max_length = 30)

	def __str__(self):
		return self.user_name

	class Meta:
		verbose_name = "Пользователь"
		verbose_name_plural = "Пользователи"
