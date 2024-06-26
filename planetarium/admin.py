from django.contrib import admin

from .models import (
    AstronomyShow,
    ShowSession,
    ShowTheme,
    PlanetariumDome,
    Reservation,
    Ticket,
)

admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(PlanetariumDome)
admin.site.register(Reservation)
admin.site.register(Ticket)
