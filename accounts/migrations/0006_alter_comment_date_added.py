# Generated by Django 3.2.3 on 2021-06-02 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date_added",
            field=models.DateTimeField(),
        ),
    ]
