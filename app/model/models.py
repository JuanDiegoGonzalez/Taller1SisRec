from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Model(models.Model) :
    MODELO_CHOICES = [
        ("Coseno", "Coseno"),
        ("Pearson", "Pearson"),
        ("Jaccard", "Jaccard")
    ]

    TIPO_CHOICES = [
        ("Usuario-Usuario", "Usuario-Usuario"),
        ("Item-Item", "Item-Item"),
    ]

    modelo = models.CharField(max_length=32,
                              choices = MODELO_CHOICES)
    tipo = models.CharField(max_length=32,
                            choices = TIPO_CHOICES)
    k = models.PositiveIntegerField()

    # Shows up in the admin list
    def __str__(self):
        return self.title