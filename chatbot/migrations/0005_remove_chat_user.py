# Generated by Django 4.2.5 on 2023-09-16 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
    ]
