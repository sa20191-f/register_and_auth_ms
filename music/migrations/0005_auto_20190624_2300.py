# Generated by Django 2.2.1 on 2019-06-24 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20190624_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertokeninfo',
            name='userID',
            field=models.ForeignKey(db_column='userID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
