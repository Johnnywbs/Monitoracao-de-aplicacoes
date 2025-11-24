from django.contrib import admin
from .models import Ingrediente, Receita, ReceitaIngrediente

admin.site.register(Ingrediente)
admin.site.register(Receita)
admin.site.register(ReceitaIngrediente)
