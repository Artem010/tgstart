# Generated by Django 3.1.4 on 2020-12-29 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201229_1941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id_user',
            new_name='tg_id',
        ),
    ]