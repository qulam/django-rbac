# Generated by Django 3.2.7 on 2021-10-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]