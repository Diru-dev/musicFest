from django.db import models
from django.conf import settings

# Create your models here.
class Artista(models.Model):
    class Genero(models.TextChoices):
        POP = "POP", "Pop"
        ROCK = "RCK", "Rock"
        METAL = "MET", "Metal"
        TECHNO = "TEC", "Techno"
        JAZZ = "JAZ", "Jazz"
        REGUETON = "REG", "Reguetón"
        OTRO = "OTR", "Otro"

    nombre = models.CharField(unique=True, max_length=30)
    pais = models.CharField(max_length=30)
    generoMusical = models.CharField(max_length=3, choices=Genero.choices, default=Genero.OTRO)
    fechaFundacion = models.DateField() #Cuando se fundo el grupo o el artista
    cache = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Escenario(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    ubicacion = models.CharField(max_length=100)
    aforo = models.PositiveIntegerField()
    cubierto = models.BooleanField(default=False)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Concierto(models.Model):
    nombre = models.CharField(max_length=100)
    fechaHora = models.DateTimeField()
    duracion = models.PositiveIntegerField() #En minutos
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    escenarios = models.ManyToManyField(Escenario, related_name="conciertos", blank=True) #Un concierto puede tener 1 o varios escenarios
    artistas = models.ManyToManyField(Artista, related_name="conciertos", blank=True) #Un concierto puede tener 1 o varios artistas, y 1 artista puede ir a uno o varios conciertos
    entradas = models.PositiveIntegerField()
    cancelado = models.BooleanField(default=False)

    class Meta:
        ordering = ["fechaHora"]

    def __str__(self):
        return f"{self.nombre} - {self.fechaHora}"


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    dni = models.CharField("DNI", max_length=9, unique=True)
    telefono = models.PositiveIntegerField(max_length=9)
    fechaNacimiento = models.DateTimeField()
    localidad = models.CharField(max_length=100)

    class Meta:
        ordering = ["usuario__username"]

    def __str__(self):
        return f"{self.usuario.username} ({self.dni})"


class 