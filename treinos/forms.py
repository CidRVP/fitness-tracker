from django import forms
from .models import Treino, ExercicioTreino, MedidasCorporais

class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['data', 'tipo_treino', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_treino': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExercicioTreinoForm(forms.ModelForm):
    class Meta:
        model = ExercicioTreino
        fields = ['exercicio', 'series', 'repeticoes', 'carga', 'ordem']
        widgets = {
            'exercicio': forms.Select(attrs={'class': 'form-control'}),
            'series': forms.NumberInput(attrs={'class': 'form-control'}),
            'repeticoes': forms.TextInput(attrs={'class': 'form-control'}),
            'carga': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ExercicioTreinoFormSet = forms.inlineformset_factory(
    Treino, ExercicioTreino, form=ExercicioTreinoForm, extra=1, can_delete=True
)

class MedidasForm(forms.ModelForm):
    class Meta:
        model = MedidasCorporais
        fields = ['data', 'peso', 'altura', 'braco_esquerdo', 'braco_direito', 
                 'peitoral', 'cintura', 'quadril', 'coxa_esquerda', 'coxa_direita']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'braco_esquerdo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'braco_direito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'peitoral': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'cintura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'quadril': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'coxa_esquerda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'coxa_direita': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }