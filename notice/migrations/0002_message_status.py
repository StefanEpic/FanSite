# Generated by Django 4.2.1 on 2023-06-06 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
