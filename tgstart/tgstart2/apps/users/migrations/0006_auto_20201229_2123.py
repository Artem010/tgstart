# Generated by Django 3.1.4 on 2020-12-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_bot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='bot_id',
        ),
        migrations.AddField(
            model_name='bot',
            name='option',
            field=models.CharField(default=0, max_length=30, verbose_name='Option'),
            preserve_default=False,
        ),
    ]
