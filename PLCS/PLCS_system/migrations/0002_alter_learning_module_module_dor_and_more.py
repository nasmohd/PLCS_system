# Generated by Django 4.1.1 on 2023-06-25 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PLCS_system", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learning_module",
            name="module_DOR",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="notification_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="last_updated",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="project_DOR",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="project_deadline",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="date_of_registration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 25, 18, 58, 6, 712382)
            ),
        ),
    ]
