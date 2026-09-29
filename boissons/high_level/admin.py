# Register your models here.
from django.contrib import admin
from .models import (
    Pays, Ville, Machine, QuantiteMachine, Lieu, Produit, Stock,
    Operation, Transport, PointDeVente, Fournisseur, PrixProduit, Facture,
)

admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Machine)
admin.site.register(QuantiteMachine)
admin.site.register(Lieu)
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Operation)
admin.site.register(Transport)
admin.site.register(PointDeVente)
admin.site.register(Fournisseur)
admin.site.register(PrixProduit)
admin.site.register(Facture)