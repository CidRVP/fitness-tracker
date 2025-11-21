from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Exercicio(models.Model):
    CATEGORIAS = [
        ('peito', 'Peito'),
        ('costas', 'Costas'),
        ('pernas', 'Pernas'),
        ('ombros', 'Ombros'),
        ('biceps', 'Bíceps'),
        ('triceps', 'Tríceps'),
        ('abdomen', 'Abdômen'),
        ('cardio', 'Cardio'),
    ]
    
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    
    def __str__(self):
        return self.nome

class Treino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    tipo_treino = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.data} - {self.tipo_treino}"

class ExercicioTreino(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.IntegerField(validators=[MinValueValidator(1)])
    repeticoes = models.CharField(max_length=20)  # Pode ser "8-12" ou "até a falha"
    carga = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    ordem = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordem']

class MedidasCorporais(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    altura = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0)])
    braco_esquerdo = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    braco_direito = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    peitoral = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    cintura = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    quadril = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    coxa_esquerda = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    coxa_direita = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['-data']
        unique_together = ['usuario', 'data']
    
    def imc(self):
        return self.peso / (self.altura * self.altura)