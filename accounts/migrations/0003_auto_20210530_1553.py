# Generated by Django 3.2.3 on 2021-05-30 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_favorite"),
    ]

    operations = [
        migrations.RenameField(
            model_name="favorite",
            old_name="product_id",
            new_name="product",
        ),
        migrations.RenameField(
            model_name="favorite",
            old_name="user_id",
            new_name="user",
        ),
    ]
