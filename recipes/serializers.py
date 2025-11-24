from rest_framework import serializers
from .models import Ingrediente, Receita, ReceitaIngrediente

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nome', 'unidade_medida']


class ReceitaIngredienteSerializer(serializers.ModelSerializer):
    # Exibindo os detalhes do ingrediente associado
    ingrediente = IngredienteSerializer()

    class Meta:
        model = ReceitaIngrediente
        fields = ['ingrediente', 'quantidade']


class ReceitaSerializer(serializers.ModelSerializer):
    # Para exibir os ingredientes com suas quantidades, usamos o relacionameto inverso
    ingredientes = ReceitaIngredienteSerializer(source='receitaingrediente_set', many=True)

    class Meta:
        model = Receita
        fields = ['id', 'nome', 'modo_preparo', 'ingredientes']

    def create(self, validated_data):
        # Extraímos os dados dos ingredientes enviados
        ingredientes_data = validated_data.pop('receitaingrediente_set')
        receita = Receita.objects.create(**validated_data)
        for item in ingredientes_data:
            ingrediente_data = item.get('ingrediente')
            # Tenta recuperar o ingrediente ou cria um novo, se não existir
            ingrediente, created = Ingrediente.objects.get_or_create(**ingrediente_data)
            ReceitaIngrediente.objects.create(
                receita=receita,
                ingrediente=ingrediente,
                quantidade=item.get('quantidade')
            )
        return receita

    def update(self, instance, validated_data):
        ingredientes_data = validated_data.pop('receitaingrediente_set', None)
        instance.nome = validated_data.get('nome', instance.nome)
        instance.modo_preparo = validated_data.get('modo_preparo', instance.modo_preparo)
        instance.save()

        if ingredientes_data is not None:
            # Para simplificar, removemos todas as relações existentes
            instance.receitaingrediente_set.all().delete()

            for item in ingredientes_data:
                ingrediente_data = item.get('ingrediente')
                ingrediente, created = Ingrediente.objects.get_or_create(**ingrediente_data)
                ReceitaIngrediente.objects.create(
                    receita=instance,
                    ingrediente=ingrediente,
                    quantidade=item.get('quantidade')
                )
        return instance
