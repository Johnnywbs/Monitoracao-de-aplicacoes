from django.db import models

class Ingrediente(models.Model):
    nome = models.CharField(max_length=255)
    unidade_medida = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Receita(models.Model):
    nome = models.CharField(max_length=255)
    modo_preparo = models.TextField()  # Modo de preparo em um único campo de texto

    # Definindo o relacionamento many-to-many com ingrediente,
    # utilizando o modelo intermediário RecipeIngredient.
    ingredientes = models.ManyToManyField(Ingrediente, through='ReceitaIngrediente')

    def __str__(self):
        return self.nome


class ReceitaIngrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.FloatField()  # Quantidade do ingrediente na receita

    def __str__(self):
        return f"{self.ingrediente.nome} em {self.receita.nome} - {self.quantidade} {self.ingrediente.unidade_medida}"