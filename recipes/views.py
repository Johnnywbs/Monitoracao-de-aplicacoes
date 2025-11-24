from rest_framework import viewsets
from .models import Ingrediente, Receita
from .serializers import IngredienteSerializer, ReceitaSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
