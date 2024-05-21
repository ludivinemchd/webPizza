from django.db import models

# Create your models here.

class Ingredient (models.Model) :
    #idIngredient est une clé primaire, n auto-incrément => AutoField
    idIngredient = models.AutoField(primary_key = True)
    #nomIngredient est une chaine de caracteres => CharField
    nomIngredient = models.CharField(max_length = 50, verbose_name = 'le nom de l ingredient')

    #une méthode de type "toString"
    def __str__(self) -> str :
        return self.nomIngredient

class Pizza(models.Model):
    #idPizza est une cle primaire, n auto-increment => AutoField
    idPizza = models.AutoField(primary_key = True)

    # nomPizza est une chaine de caractere => CharField
    nomPizza = models.CharField(max_length = 50, verbose_name='le nom de cette pizza')

    #le prix est decimal, maximum = 4 chiffres, dont 2 decimales
    prix = models.DecimalField(max_digits = 4, decimal_places = 2, verbose_name = 'le prix')

    #fichier image de la pizza
    image = models.ImageField(default = 'imagesPizzas/delfault.PNG', upload_to = 'imagesPizzas/')
    # une methode de type "toString"
    def __str__(self) -> str :
        return 'pizza ' + self.nomPizza + ' (prix: '+ str(self.prix) + '€)'

class Composition (models.Model) :

    #la classe Meta qui gere l'unicite du couple de cles etrangeres
    class Meta :
        unique_together = ('ingredient','pizza')  #le nom des champs des cles etrangeres

    #idComposition est la cles primaire
    idComposition = models.AutoField(primary_key= True)

    #les deux champs cles etrangeres, dont les noms correspondent
    #aux classes respectives en minuscule

    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete = models.CASCADE)

    #l'autre champs, chaine de caracteres
    quantite = models.CharField(max_length=100, verbose_name = 'la quantite')

    #une methode de type toString
    def __str__(self) -> str :
        ing = self.ingredient
        piz = self.pizza
        return ing.nomIngredient + ' fait partie de la pizza ' + piz.nomPizza+ ' (quantite :' + self.quantite +')'

