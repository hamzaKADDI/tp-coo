# Create your views here.
from django.http import JsonResponse
from django.views.generic import DetailView

from .models import (
    Facture, Fournisseur, Lieu, Machine, Operation, Pays, PointDeVente,
    PrixProduit, Produit, QuantiteMachine, Stock, Transport, Ville,
)


class JsonDetailView(DetailView):
    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json(), **response_kwargs)


class PaysView(JsonDetailView): model = Pays
class VilleView(JsonDetailView): model = Ville
class MachineView(JsonDetailView): model = Machine
class QuantiteMachineView(JsonDetailView): model = QuantiteMachine
class LieuView(JsonDetailView): model = Lieu
class ProduitView(JsonDetailView): model = Produit
class StockView(JsonDetailView): model = Stock
class OperationView(JsonDetailView): model = Operation
class TransportView(JsonDetailView): model = Transport
class PointDeVenteView(JsonDetailView): model = PointDeVente
class FournisseurView(JsonDetailView): model = Fournisseur
class PrixProduitView(JsonDetailView): model = PrixProduit
class FactureView(JsonDetailView): model = Facture


# Optionnel : JSON étendu
#class ApiView(DetailView):
 #   model = Lieu

  #  def render_to_response(self, context, **response_kwargs):
   #     return JsonResponse(self.object.json_extended(), **response_kwargs)