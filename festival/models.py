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
        constraints = [
            models.CheckConstraint(condition=models.Q(cache__gte=0), name="cache_mayor_0")
        ]

    def __str__(self):
        return self.nombre


class Escenario(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    ubicacion = models.CharField(max_length=100)
    aforo = models.PositiveIntegerField()
    cubierto = models.BooleanField(default=False)

    class Meta:
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(condition=models.Q(aforo__gt=0), name="aforo_mayor_0")
        ]

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
        constraints = [
            models.CheckConstraint(condition=models.Q(duracion__gt=0), name="duracion_mayor_0"),
            models.CheckConstraint(condition=models.Q(precio__gte=0), name="precio_mayor_0")
        ]

    def __str__(self):
        return f"{self.nombre} - {self.fechaHora}"


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    dni = models.CharField("DNI", max_length=9, unique=True)
    telefono = models.CharField(max_length=15)
    fechaNacimiento = models.DateField()
    localidad = models.CharField(max_length=100)

    class Meta:
        ordering = ["usuario__username"]

    def __str__(self):
        return f"{self.usuario.username} ({self.dni})"


class Reserva(models.Model):
    localizador = models.CharField(max_length=9, unique=True, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas")
    concierto = models.ForeignKey(Concierto, on_delete=models.PROTECT, related_name="reservas")
    fechaReserva = models.DateTimeField(auto_now_add=True)
    numeroEntradas = models.PositiveIntegerField()
    importeTotal = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True) #True -> Confirmada | False -> Cancelada

    class Meta:
        ordering = ["-fechaReserva"]
        constraints = [
            models.CheckConstraint(condition=models.Q(numeroEntradas__gte=1), name="mas_de_1_entrada"),
            models.CheckConstriant(condition=models.Q(importeTotal__gte=1), name="importe_mayor_1")
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.localizador}"