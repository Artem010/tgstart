# Generated by Django 3.1.4 on 2020-12-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_email',
            field=models.CharField(default=0, max_length=30, verbose_name='Email'),
            preserve_default=False,
        ),
    ]