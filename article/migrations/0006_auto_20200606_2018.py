# Generated by Django 3.0.6 on 2020-06-06 14:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='readers',
            field=models.ManyToManyField(blank=True, related_name='articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
