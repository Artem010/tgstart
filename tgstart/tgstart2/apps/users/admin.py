from django.contrib import admin

# Register your models here.
from .models import User
from .models import Bot
from .models import Messages

admin.site.register(User)
admin.site.register(Bot)
admin.site.register(Messages)
