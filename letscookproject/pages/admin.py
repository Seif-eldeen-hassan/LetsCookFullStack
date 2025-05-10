from django.contrib import admin
from .models import userDB,RecipeDB,IngredientDB,FavouriteRecipeDB

admin.site.register(userDB)
admin.site.register(RecipeDB)
admin.site.register(IngredientDB)
admin.site.register(FavouriteRecipeDB)