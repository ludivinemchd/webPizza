from django.shortcuts import render
#import des modeles
from applipizza.models import Pizza
from applipizza.models import Ingredient
from applipizza.models import Composition
from applipizza.forms import IngredientForm
from applipizza.forms import PizzaForm
from applipizza.forms import CompositionForm
# Create your views here.
def pizzas(request):
    #recuperation des pizzas de la base de donnees
    # avec les memes instructions que dans le shell
    lesPizzas = Pizza.objects.all()

    #on retourne l'emplacement du template et meme,
    #s'il ne sert pas cette fois, le parametre,
    #request, ainsi que le contenu calcule (lesPizzas)
    #sous forme d'un dictionnaire python

    return render(
        request,
        'applipizza/pizzas.html',
        {'pizzas': lesPizzas}
    )

def ingredients(request):
    #recuperation des ingredients de la base de donnees
    # avec les memes instructions que dans le shell
    lesIngredients = Ingredient.objects.all()

    #on retourne l'emplacement du template et meme,
    #s'il ne sert pas cette fois, le parametre,
    #request, ainsi que le contenu calcule (lesPizzas)
    #sous forme d'un dictionnaire python

    return render(
        request,
        'applipizza/ingredients.html',
        {'ingredients': lesIngredients}
    )

def pizza(request, pizza_id) :
    #recuperation de la pizza dont l'indentifiant a ete passé en parametre (c'est l'int pizza_id)
    laPizza = Pizza.objects.get(idPizza = pizza_id)

    #recuperation des ingredients entrant dans la composition de la pizza
    compo = Composition.objects.filter(pizza = pizza_id)

    lesIng = Ingredient.objects.all()
    #on cree un dictionnaire dont chaque item sera lui-meme
    #un dictionnaire contenant :
    #-l'identfiant de la composition (idComposition)
    #-le nom de l'ingredient
    #-la quantite de l'ingredient de la composition

    #on retourne l'emplacement du template et la pizza recuperee de la bd et la liste des ingredients ci dessus
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza" : laPizza, "ingredients" : compo, 'lesIng' : lesIng}
    )

def formulaireCreationIngredient(request):
    #on retourne l'emplacement template
    return render(
        request,
        'applipizza/formulaireCreationIngredient.html',
    )

def creerIngredient(request):

    #recuperation du formulaire posté
    form = IngredientForm(request.POST)

    if form.is_valid():
        #recuperation de la valeur du champ 'nomIngredient'
        #form.cleaned_data permet de nettoyer la donnée au cas ou
        #des injections en tout genre seraient presentes
        nomIng = form.cleaned_data['nomIngredient']

        #creation d'un nouvel infredient
        ing = Ingredient()

        #affectation de son attribut nomIngredient
        ing.nomIngredient = nomIng

        #enregistrement de l'ingredient dans la base
        ing.save()

        #on retourne l'emplacement de la vue (ou plutot du template,
        #au sens de django) et le conrtenu calculé,
        #sous forme de dictionnaire

    return render(
        request,
        'applipizza/traitementFormulaireCreationIngredient.html',
        {"nom": nomIng}
    )

def formulaireCreationPizza(request):
    #on retourne l'emplacement template
    return render(
        request,
        'applipizza/formulaireCreationPizza.html',
    )

def creerPizza(request):

    #recuperation du formulaire posté
    form = PizzaForm(request.POST, request.FILES)
    print (form)
    if form.is_valid():
        #recuperation de la valeur du champ 'nomPizza'
        #form.cleaned_data permet de nettoyer la donnée au cas ou
        #des injections en tout genre seraient presentes
        nomPiz = form.cleaned_data['nomPizza']
        prixPiz = form.cleaned_data['prix']
        #creation d'une nouvelle pizza
        piz = Pizza()

        #affectation de son attribut nomPiz
        piz.nomPizza = nomPiz
        piz.prix = prixPiz
        piz.image = request.FILES['image']
        #enregistrement de la pizza dans la base
        piz.save()

        #on retourne l'emplacement de la vue (ou plutot du template,
        #au sens de django) et le conrtenu calculé,
        #sous forme de dictionnaire

    return render(
        request,
        'applipizza/traitementFormulaireCreationPizza.html',
        {"nom": nomPiz, "prix": prixPiz}
    )

def ajouterIngredientDansPizza(request,pizza_id):
    #recuperation du formulaire posté
    formulaire = CompositionForm(request.POST)

    if formulaire.is_valid():
        #recuperation des donnees postees
        ing = formulaire.cleaned_data['ingredient']

        qte = formulaire.cleaned_data['quantite']

        laPizza = Pizza.objects.get(idPizza = pizza_id)

        compoPizza = Composition.objects.filter(pizza = pizza_id)

        lesIngredientsDeLaPizza = ((ligne.ingredient) for ligne in compoPizza)

    if ing in lesIngredientsDeLaPizza:
        compo = Composition.objects.filter(pizza = pizza_id, ingredient =ing)
        compo.delete()

    #creation de la nouvelle instance de Composition et remplissage de ses attributs
    compo = Composition()
    compo.ingredient = ing
    compo.pizza = laPizza
    compo.quantite = qte
    #sauvegarde dans la base de la composition
    compo.save()

    #recuperation de tous les ingredients pour construire le futur select 
    lesIngredients = Ingredient.objects.all()
    #actualisation des ingredients entrant dans la composition de la pizza
    compoPizza = Composition.objects.filter(pizza = pizza_id)
    #on crée une liste dont chaque item contiendra l'identifiant de la composition (idComposition),
    # le nom de l'ingrédient et la quantite de l'ingredient dans cette composition
    listeIngredients = []
    for ligneCompo in compoPizza:
        #on recupere l'Ingredient pour utiliser son nomIngredient
        ingredient = Ingredient.objects.get(idIngredient = ligneCompo.ingredient.idIngredient)
        listeIngredients.append(
            {"idComposition" : ligneCompo.idComposition, "nom" : ingredient.nomIngredient, "qte" : ligneCompo.quantite}
        )
    #on retourne l'emplacement du temmplate, la pizza recuperee et la liste des ingredients calculées ci dessus
    return render(
        request,
        'applipizza/pizza.html',
        { "liste" : listeIngredients, "pizza" : laPizza, "ingredients" : compoPizza,"lesIng" : lesIngredients}
    )

def supprimerPizza(request,pizza_id):
    #récupére la pizza à supprimer
    laPizza = Pizza.objects.get(idPizza = pizza_id)

    #appel de la méthode delete() sur cette pizza,
    laPizza.delete()

    #récupére la liste de toutes les pizzas
    lesPizzas = Pizza.objects.all()

    #appel du template pizzas.html
    return render(
        request,
        'applipizza/pizzas.html',
        {'pizzas': lesPizzas}
    )

def afficherFormulaireModificationPizza(request, pizza_id):
    #récupére la pizza à afficher dans le formulaire
    pizza_a_modifier = Pizza.objects.get(idPizza = pizza_id)
    #appel formulaireModificationpizza.html
    return render (
        request,
        "applipizza/formulaireModificationPizza.html",
        {"pizza" : pizza_a_modifier}
    )

def modifierPizza(request, pizza_id):
    #récupére la pizza à afficher dans le formulaire
    pizza_a_modifier = Pizza.objects.get(idPizza = pizza_id)

    #recuperation du nom ,de la pizza avant la modification
    nomPiz = pizza_a_modifier.nomPizza 
    #récupération formulaire posté 
    form = PizzaForm(request.POST, request.FILES, instance = pizza_a_modifier)

    if form.is_valid():
       pizza_a_modifier.image= request.FILES['image']
       form.save()

    return render (
        request,
        "applipizza/traitementFormulaireModificationPizza.html",
        {"nomAvant" : nomPiz}
    ) 
        
def supprimerIngredient(request,ingredient_id):
    #récupére la pizza à supprimer
    lingredient = Ingredient.objects.get(idIngredient = ingredient_id)

    #appel de la méthode delete() sur cette pizza,
    lingredient.delete()

    #récupére la liste de toutes les pizzas
    lesIngredients = Ingredient.objects.all()

    #appel du template pizzas.html
    return render(
        request,
        'applipizza/ingredients.html',
        {'ingredients': lesIngredients}
    )

def afficherFormulaireModificationIngredient(request, ingredient_id):
    #récupére la pizza à afficher dans le formulaire
    ingredient_a_modifier = Ingredient.objects.get(idIngredient = ingredient_id)
    #appel formulaireModificationpizza.html
    return render (
        request,
        "applipizza/formulaireModificationIngredient.html",
        {"ingredient" : ingredient_a_modifier}
    )

def modifierIngredient(request, ingredient_id):
    #récupére la pizza à afficher dans le formulaire
    ingredient_a_modifier = Ingredient.objects.get(idIngredient = ingredient_id)

    #recuperation du nom ,de la pizza avant la modification
    nomIng = ingredient_a_modifier.nomIngredient
    #récupération formulaire posté 
    form = IngredientForm(request.POST, instance = ingredient_a_modifier)

    if form.is_valid():
       form.save()

    return render (
        request,
        "applipizza/traitementFormulaireModificationIngredient.html",
        {"nomAvant" : nomIng}
    ) 

def supprimerIngredientDansPizza(request, pizza_id, composition_id):
    #récupére la composition à supprimer
    laCompo = Composition.objects.get(idComposition = composition_id)
    laCompo.delete()
    laPizza = Pizza.objects.get(idPizza = pizza_id)
    compoPizza = Composition.objects.filter(pizza = pizza_id)
    listeIngredients = []
    for ligneCompo in compoPizza:
        #on recupere l'Ingredient pour utiliser son nomIngredient
        ingredient = Ingredient.objects.get(idIngredient = ligneCompo.ingredient.idIngredient)
        listeIngredients.append(
            {"idComposition" : ligneCompo.idComposition, "nom" : ingredient.nomIngredient, "qte" : ligneCompo.quantite}
        )
    
   # formulaire = CompositionForm()
    return render(
        request,
        'applipizza/pizza.html',
        {"pizza" : laPizza, "ingredients" : compoPizza, "liste" : listeIngredients}
    )
