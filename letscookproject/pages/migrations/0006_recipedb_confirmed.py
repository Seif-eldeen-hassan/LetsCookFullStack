# Generated by Django 5.2.1 on 2025-05-09 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_rename_ingredient_ingredientdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipedb',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
