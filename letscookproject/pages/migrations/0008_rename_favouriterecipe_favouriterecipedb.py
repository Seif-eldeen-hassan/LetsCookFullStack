# Generated by Django 5.2.1 on 2025-05-09 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_favouriterecipe'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavouriteRecipe',
            new_name='FavouriteRecipeDB',
        ),
    ]
