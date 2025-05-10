from django.shortcuts import render , redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json , random


from .models import userDB,RecipeDB,IngredientDB,FavouriteRecipeDB


def home(request):
    user = None
    is_admin = False
    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass

    confirmed_recipes = RecipeDB.objects.filter(confirmed=True)

    latest_recipes = confirmed_recipes.order_by('-created_at')[:3]
    
    all_recipes = list(confirmed_recipes)
    random_recipes = random.sample(all_recipes, min(3, len(all_recipes)))
    fav_ids = list(FavouriteRecipeDB.objects.filter(user=user).values_list('recipe_id', flat=True))

    return render(request, 'pages/home.html', {
        'user': user,
        'is_admin': is_admin,
        'recipes': confirmed_recipes,       
        'latest_recipes': latest_recipes,    
        'random_recipes': random_recipes,
        'fav_ids': fav_ids     
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('agree') == 'on'
        user = userDB.objects.create(username=username, email=email, password=password, is_admin =is_admin )
        request.session['user_id'] = user.id
        return redirect('home')
    return render(request, 'pages/signup.html')



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = userDB.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, "Invalid Password.")
                return redirect('signin')

        except userDB.DoesNotExist:   
            messages.error(request, "No account with that email exists.")
            return redirect('signin')

    return render(request, 'pages/login.html')


def add_ingredient_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            amount = data.get('amount')
            recipe_id = data.get('recipe_id')

            recipe = RecipeDB.objects.get(id=recipe_id)
            ingredient = IngredientDB.objects.create(
                recipe=recipe,
                name=name,
                amount=amount
            )

            return JsonResponse({'success': True, 'ingredient_id': ingredient.id})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def delete_ingredient_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredient_id = data.get('id')
            IngredientDB.objects.get(id=ingredient_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})



def addrecipe(request):
    user = None
    is_admin = False
    recipe = None

    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass  
        
        if request.method == 'POST':
            recipe_id = request.POST.get('recipe_id')
            name = request.POST.get('recipe_name')
            course = request.POST.get('course')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            try:
                recipe = RecipeDB.objects.get(id=recipe_id)
                recipe.RecipeName = name
                recipe.Course = course
                recipe.description = description
                recipe.confirmed = True
                if image:
                    recipe.RecipeImage = image
                recipe.save()
                return redirect('home')  
            except RecipeDB.DoesNotExist:
                return redirect('addrecipe')  

        else:
            RecipeDB.objects.filter(user=user, confirmed=False).delete()
            recipe = RecipeDB.objects.create(user=user, RecipeName='', Course='', description='')
            print("created Recipe")

    return render(request, 'pages/addrecipe.html', {
        'user': user,
        'is_admin': is_admin,
        'recipe': recipe
    })

def recipes(request):
    user = None
    is_admin = False
    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass
    recipes = RecipeDB.objects.filter(confirmed=True)
    fav_ids = list(FavouriteRecipeDB.objects.filter(user=user).values_list('recipe_id', flat=True))

    return render(request, 'pages/recipes.html', {
        'user': user,
        'is_admin': is_admin,
        'recipes': recipes,
        'fav_ids': fav_ids 
    })


def myrecipes(request):
    user = None
    is_admin = False
    recipes = RecipeDB.objects.none()

    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
            recipes = RecipeDB.objects.filter(user=user, confirmed=True)
        except userDB.DoesNotExist:
            pass

    return render(request, 'pages/myrecipes.html', {
        'user': user,
        'is_admin': is_admin,
        'recipes': recipes
    })



def ingredients(request, recipe_id):
    user = None
    is_admin = False
    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass
    recipe = get_object_or_404(RecipeDB, id=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'pages/ingeridents.html', { 
        'user': user,
        'is_admin': is_admin,
        'recipe': recipe,
        'ingredients': ingredients
    })


def account(request):
    user = None
    is_admin = False
    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass

    return render(request, 'pages/account.html', {'user': user, 'is_admin': is_admin})


@csrf_exempt
@require_POST
def toggle_favourite(request):
    try:
        data = json.loads(request.body)
        recipe_id = data.get('recipe_id')
        user_id = request.session.get('user_id')

        if not user_id:
            return JsonResponse({'success': False, 'error': 'Not logged in'})

        user = userDB.objects.get(id=user_id)
        recipe = RecipeDB.objects.get(id=recipe_id)

        fav, created = FavouriteRecipeDB.objects.get_or_create(user=user, recipe=recipe)

        if not created:
            fav.delete()
            return JsonResponse({'success': True, 'favorited': False})
        return JsonResponse({'success': True, 'favorited': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def favourites(request):
    user = None
    is_admin = False
    if 'user_id' in request.session:
        try:
            user = userDB.objects.get(id=request.session['user_id'])
            is_admin = user.is_admin
        except userDB.DoesNotExist:
            pass
    recipes = RecipeDB.objects.filter(confirmed=True)
    fav_ids = list(FavouriteRecipeDB.objects.filter(user=user).values_list('recipe_id', flat=True))

    return render(request, 'pages/favourites.html', {
        'user': user,
        'is_admin': is_admin,
        'recipes': recipes,
        'fav_ids': fav_ids 
    })


@csrf_exempt
@require_POST
def delete_recipe_ajax(request):
    try:
        data = json.loads(request.body)
        recipe_id = data.get('recipe_id')
        user_id = request.session.get('user_id')

        if not user_id:
            return JsonResponse({'success': False, 'error': 'User not authenticated'})

        recipe = RecipeDB.objects.get(id=recipe_id, user_id=user_id)
        recipe.delete()
        return JsonResponse({'success': True})

    except RecipeDB.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Recipe not found'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    
def edit_recipe(request, recipe_id):
    user = userDB.objects.get(id=request.session['user_id'])
    is_admin = user.is_admin

    recipe = get_object_or_404(RecipeDB, id=recipe_id, user=user)
    ingredients = IngredientDB.objects.filter(recipe=recipe)

    if request.method == 'POST':
        recipe.RecipeName = request.POST.get('recipe_name', '')
        recipe.Course = request.POST.get('course', '')
        recipe.description = request.POST.get('description', '')
        image = request.FILES.get('image')
        if image:
            recipe.RecipeImage = image
        recipe.confirmed = True
        recipe.save()
        return redirect('home')

    return render(request, 'pages/addrecipe.html', {
        'user': user,
        'is_admin': is_admin,
        'recipe': recipe,
        'ingredients': ingredients
    })