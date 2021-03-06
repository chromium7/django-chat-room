# Generated by Django 3.1.6 on 2021-02-13 03:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='bruh', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(related_name='rooms_joined', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='moderator',
            field=models.ManyToManyField(related_name='rooms_moderated', to=settings.AUTH_USER_MODEL),
        ),
    ]
