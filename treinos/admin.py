from django.contrib import admin
from .models import Exercicio, Treino, ExercicioTreino, MedidasCorporais

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria']
    list_filter = ['categoria']

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data', 'tipo_treino']
    list_filter = ['data']

@admin.register(ExercicioTreino)
class ExercicioTreinoAdmin(admin.ModelAdmin):
    list_display = ['treino', 'exercicio', 'series', 'repeticoes', 'carga']

@admin.register(MedidasCorporais)
class MedidasCorporaisAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data', 'peso', 'altura']