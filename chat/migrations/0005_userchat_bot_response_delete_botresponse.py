# Generated by Django 5.0.2 on 2024-03-16 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_rename_chathistory_userchat_botresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchat',
            name='bot_response',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='BotResponse',
        ),
    ]