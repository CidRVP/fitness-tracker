from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Max, Avg
from .models import Treino, ExercicioTreino, Exercicio, MedidasCorporais
from .forms import TreinoForm, ExercicioTreinoFormSet, MedidasForm
from datetime import date, timedelta
import json

@login_required
def dashboard(request):
    # Últimos treinos
    ultimos_treinos = Treino.objects.filter(usuario=request.user)[:5]
    
    # Estatísticas básicas
    total_treinos = Treino.objects.filter(usuario=request.user).count()
    
    # Preparar dados para gráfico de progresso de carga
    dados_carga = []
    exercicios_principais = Exercicio.objects.filter(
        exerciciotreino__treino__usuario=request.user
    ).distinct()[:5]
    
    for exercicio in exercicios_principais:
        # Pegar os últimos 5 registros de cada exercício
        historico = ExercicioTreino.objects.filter(
            exercicio=exercicio,
            treino__usuario=request.user
        ).order_by('-treino__data')[:5]  # Ordenar do mais recente para o mais antigo
        
        if historico:
            # Reverter para mostrar em ordem cronológica no gráfico
            historico_ordenado = list(reversed(historico))
            dados_carga.append({
                'exercicio': exercicio.nome,
                'datas': [h.treino.data.strftime('%d/%m') for h in historico_ordenado],
                'cargas': [float(h.carga) for h in historico_ordenado]
            })
    
    # Se não houver dados, criar dados de exemplo vazios
    if not dados_carga:
        dados_carga = [{
            'exercicio': 'Sem dados',
            'datas': [],
            'cargas': []
        }]
    
    context = {
        'ultimos_treinos': ultimos_treinos,
        'total_treinos': total_treinos,
        'dados_carga_json': json.dumps(dados_carga),
    }
    return render(request, 'treinos/dashboard.html', context)

@login_required
def criar_treino(request):
    if request.method == 'POST':
        form = TreinoForm(request.POST)
        formset = ExercicioTreinoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            treino = form.save(commit=False)
            treino.usuario = request.user
            treino.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.treino = treino
                instance.save()
            
            messages.success(request, 'Treino salvo com sucesso!')
            return redirect('dashboard')
    else:
        # Auto-fill com último treino
        ultimo_treino = Treino.objects.filter(usuario=request.user).first()
        if ultimo_treino:
            initial_data = {'tipo_treino': ultimo_treino.tipo_treino}
            form = TreinoForm(initial=initial_data)
        else:
            form = TreinoForm()
        
        formset = ExercicioTreinoFormSet()
    
    return render(request, 'treinos/criar_treino.html', {
        'form': form,
        'formset': formset
    })

@login_required
def historico_treinos(request):
    treinos = Treino.objects.filter(usuario=request.user)
    return render(request, 'treinos/historico.html', {'treinos': treinos})

@login_required
def detalhes_treino(request, treino_id):
    treino = get_object_or_404(Treino, id=treino_id, usuario=request.user)
    return render(request, 'treinos/detalhes_treino.html', {'treino': treino})

@login_required
def medidas_corporais(request):
    if request.method == 'POST':
        form = MedidasForm(request.POST)
        if form.is_valid():
            medidas = form.save(commit=False)
            medidas.usuario = request.user
            medidas.save()
            messages.success(request, 'Medidas salvas com sucesso!')
            return redirect('medidas_corporais')
    else:
        form = MedidasForm()
    
    historico_medidas = MedidasCorporais.objects.filter(usuario=request.user)
    
    # Dados para gráfico de progresso
    dados_progresso = {
        'datas': [str(m.data) for m in historico_medidas],
        'pesos': [float(m.peso) for m in historico_medidas],
        'imc': [float(m.imc()) for m in historico_medidas]
    }
    
    return render(request, 'treinos/medidas.html', {
        'form': form,
        'historico_medidas': historico_medidas,
        'dados_progresso_json': json.dumps(dados_progresso)
    })

@login_required
def comparar_performance(request):
    exercicios = Exercicio.objects.filter(
        exerciciotreino__treino__usuario=request.user
    ).distinct()
    
    dados_comparacao = []
    
    if request.method == 'POST':
        exercicio_id = request.POST.get('exercicio')
        if exercicio_id:
            exercicio = get_object_or_404(Exercicio, id=exercicio_id)
            
            # Buscar registros mais antigos e mais recentes
            registros = ExercicioTreino.objects.filter(
                exercicio=exercicio,
                treino__usuario=request.user
            ).order_by('treino__data')
            
            if registros.count() >= 2:
                primeiro = registros.first()
                ultimo = registros.last()
                
                dados_comparacao = {
                    'exercicio': exercicio.nome,
                    'primeiro': {
                        'data': primeiro.treino.data,
                        'carga': primeiro.carga,
                        'series': primeiro.series,
                        'repeticoes': primeiro.repeticoes
                    },
                    'ultimo': {
                        'data': ultimo.treino.data,
                        'carga': ultimo.carga,
                        'series': ultimo.series,
                        'repeticoes': ultimo.repeticoes
                    },
                    'progresso_carga': float(ultimo.carga - primeiro.carga),
                    'progresso_percentual': float(((ultimo.carga - primeiro.carga) / primeiro.carga) * 100)
                }
    
    return render(request, 'treinos/comparar.html', {
        'exercicios': exercicios,
        'dados_comparacao': dados_comparacao
    })