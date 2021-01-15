from django.db import models


class User(models.Model):
	user_name = models.CharField('Логин', max_length = 30)
	user_firstname = models.TextField('Имя', max_length = 30)
	user_lastname = models.TextField('Фамилия', max_length = 30)
	tg_id = models.CharField('tg_id', max_length = 10)


	def __str__(self):
		return self.user_name

	class Meta:
		verbose_name = "Пользователь"
		verbose_name_plural = "Пользователи"

class Bot(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	# bot_id = models.CharField('bot_id', max_length = 30)
	option = models.CharField('Option', max_length = 30)
	bot_name = models.CharField('Bot Name', max_length = 30)
	token = models.CharField('Token', max_length = 100)
	status = models.IntegerField('Status', default=1)

	def __str__(self):
		return (str(self.id) + "_" + str(self.user))

	class Meta:
		verbose_name = "Бот"
		verbose_name_plural = "Боты"

class Messages(models.Model):
	bot_name = models.ForeignKey(Bot, on_delete = models.CASCADE)
	count = models.IntegerField('Count', default=0)
	date = models.CharField('Date', max_length = 30)
