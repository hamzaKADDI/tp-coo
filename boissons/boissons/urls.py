"""
URL configuration for boissons project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from high_level import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
        path("pays/<int:pk>", views.PaysView.as_view()),
    path("ville/<int:pk>", views.VilleView.as_view()),
    path("machine/<int:pk>", views.MachineView.as_view()),
    path("quantite-machine/<int:pk>", views.QuantiteMachineView.as_view()),
    path("lieu/<int:pk>", views.LieuView.as_view()),
    path("produit/<int:pk>", views.ProduitView.as_view()),
    path("stock/<int:pk>", views.StockView.as_view()),
    path("operation/<int:pk>", views.OperationView.as_view()),
    path("transport/<int:pk>", views.TransportView.as_view()),
    path("point-de-vente/<int:pk>", views.PointDeVenteView.as_view()),
    path("fournisseur/<int:pk>", views.FournisseurView.as_view()),
    path("prix-produit/<int:pk>", views.PrixProduitView.as_view()),
    path("facture/<int:pk>", views.FactureView.as_view()),
    #path("api/<int:pk>", views.ApiView.as_view()),
]
