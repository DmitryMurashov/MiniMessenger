# Generated by Django 4.0.6 on 2022-07-30 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_chatinvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmember',
            name='chat_custom_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
