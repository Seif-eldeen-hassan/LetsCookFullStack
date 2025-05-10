from django.db import models

class userDB(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username} ({self.email})"
    

class RecipeDB(models.Model):
    user = models.ForeignKey(userDB, on_delete=models.CASCADE, related_name='recipes')
    RecipeName  = models.CharField(max_length=100)
    Course = models.CharField(max_length=100)
    description = models.TextField()
    RecipeImage = models.ImageField(
        upload_to='recipe_images',
        null=True,
        blank=True,
        default='recipe_images/b170870007dfa419295d949814474ab2_t.jpg'  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.RecipeName} by {self.user.username}"
    
    
class IngredientDB(models.Model):
    recipe = models.ForeignKey(RecipeDB, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.amount} of {self.name}"
    

class FavouriteRecipeDB(models.Model):
    user = models.ForeignKey(userDB, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(RecipeDB, on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe') 

    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.RecipeName}"
