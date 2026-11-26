# PROYECTO PRÁCTICA DJANGO
- Proyecto de práctica de Django simulación de exámen.

# Comandos de la shell
from datetime import date
fantasm = Artista.objects.create(
    nombre="Fantasm",
    pais="Francia",
    generoMusical="TEC",
    fechaFundacion=date.today(),
    cache=100,
    activo=True,
)

davidBisbal = Artista.objects.create(
    nombre="David Bisbal",
    pais="España",
    generoMusical="POP",
    fechaFundacion=date.today(),
    cache=70,
    activo=True,
)

escenario1 = Escenario.objects.create(
    nombre="Blackworks",
    ubicacion="IFEMA",
    aforo=50000,
    cubierto=True,
)

concierto = Concierto.objects.create(
    nombre="My summer Story",
    fechaHora=date.today(),
    descripcion="Evento en Madrid en el IFEMA, con un escenario de la marca Blackworks. Su cabeza de cartel es el conocido FANTASM",
    precio=60,
    entradas=50000,
    cancelado=False,
)

concierto.escenarios.add(escenario1)
concierto.artistas.add(fantasm, davidBisbal)

artistaRecuperado = Artista.objects.get(pk=fantasm.pk)

reserva1 = Reserva.objects.create(
    localizador="ABC123456",
    usuario=get_user_model(),
    concierto=concierto,
    fechaReserva=date.today(),
    numeroEntradas=1,
    importeTotal=60,
    estado=True
)
reservaRecuperada = Reserva.get(localizador="ABC123456")

Concierto.objects.filter(nombre="My summer Story").update(precio=55)

escenario2 = Escenario.objects.create(
    nombre="Bresh",
    ubicacion="IFEMA",
    aforo=30000,
    cubierto=False,
)

Concierto.objects.filter(nombre="My summer Story").update(escenario=escenario2, cancelado=True)



## Autor
- Carlos Sánchez Damas