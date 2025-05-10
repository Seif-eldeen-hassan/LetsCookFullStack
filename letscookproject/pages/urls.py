from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('addrecipe/', views.addrecipe, name='addrecipe'),
    path('ajax/add-ingredient/', views.add_ingredient_ajax, name='add_ingredient_ajax'),
    path("ajax/delete-ingredient/", views.delete_ingredient_ajax, name="delete_ingredient_ajax"),
    path('recipes/', views.recipes, name='recipes'),
    path('myrecipes/', views.myrecipes, name='myrecipes'),
    path('account/', views.account, name='account'),
    path('recipes/<int:recipe_id>/ingredients', views.ingredients, name='ingredients'),
    path('ajax/toggle-fav/', views.toggle_favourite, name='toggle_fav'),
    path('favourites/', views.favourites, name='favourites'),
    path("ajax/delete-recipe/", views.delete_recipe_ajax, name="delete_recipe_ajax"),
    path('recipes/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
