# Generated by Django 4.0.6 on 2022-07-29 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_chat_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='image',
            field=models.ImageField(default='https://sun1-47.userapi.com/s/v1/if1/f-xqnN-x7i5-U-Kq3VRTt2h7m6dJT6K-XVVq0py6Yg9WOB2fhACUc3U3gOLbsbodwfzSwHbi.jpg?size=400x0&quality=96&crop=5,0,236,236&ava=1', upload_to=''),
        ),
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(default='Chat', max_length=50),
        ),
    ]
