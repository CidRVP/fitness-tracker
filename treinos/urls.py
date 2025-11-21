from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('treino/novo/', views.criar_treino, name='criar_treino'),
    path('treino/historico/', views.historico_treinos, name='historico_treinos'),
    path('treino/<int:treino_id>/', views.detalhes_treino, name='detalhes_treino'),
    path('medidas/', views.medidas_corporais, name='medidas_corporais'),
    path('comparar/', views.comparar_performance, name='comparar_performance'),
]