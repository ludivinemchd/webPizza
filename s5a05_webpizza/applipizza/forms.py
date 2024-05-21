from django import forms
from django.forms import ModelForm
from applipizza.models import Ingredient
from applipizza.models import Pizza
from applipizza.models import Composition

class IngredientForm(ModelForm):
    class Meta :
        model = Ingredient
        fields = ['nomIngredient']
        
###la version non-automatique, où on déclare les
#champs équivalents à ceux de la classe.
#class IngredientForm(forms.Form):
#   nomIngredient = forms.CharField(
#       label = 'nom de cet ingredient',
#       max_length = 50 
#   )
###


class PizzaForm(ModelForm):
    class Meta :
        model = Pizza
        fields = ['nomPizza','prix']

class CompositionForm(ModelForm):
    class Meta :
        model = Composition
        fields = ['ingredient','quantite']
