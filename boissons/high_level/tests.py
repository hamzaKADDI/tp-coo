from django.test import TestCase

from .models import (
    Fournisseur,
    Lieu,
    Machine,
    Pays,
    PointDeVente,
    PrixProduit,
    Produit,
    QuantiteMachine,
    Stock,
    Ville,
)



ATTENDU = 111_000


class MachineModelTests(TestCase):
    def test_machine_creation(self):
        self.assertEqual(Machine.objects.count(), 0)
        Machine.objects.create(
            nom="CNC", prix=28_000, duree_de_vie=10, cout_maintenance=500, superficie=6
        )
        self.assertEqual(Machine.objects.count(), 1)


class ScenarioCoutsTests(TestCase):
    def test_cout_du_lieu(self):
  
        france = Pays.objects.create(
            nom="France", tva=20, tarif_electrique=20, salaire_minimum=12
        )

        labege = Ville.objects.create(
            nom="Labège", taxe_immobiliere=0, prix_m2=2_000, pays=france
        )

        lieu = Lieu.objects.create(
            nom="Usine", ville=labege, superficie=50, consommation_electrique=5_000
        )

       
        m1 = Machine.objects.create(
            nom="M1", prix=10_000, duree_de_vie=10, cout_maintenance=0, superficie=5
        )
        m2 = Machine.objects.create(
            nom="M2", prix=5_000, duree_de_vie=10, cout_maintenance=0, superficie=5
        )
        lieu.machines.set([
            QuantiteMachine.objects.create(machine=m1, nombre=1),
            QuantiteMachine.objects.create(machine=m2, nombre=1),
        ])

        fournisseur = Fournisseur.objects.create(nom="Fournisseur")
        tubes = Produit.objects.create(
            nom="Palette de tubes d'acier",
            prix_de_vente=0, duree_de_vie=10, nombre_par_palette=1,
        )
        cables = Produit.objects.create(
            nom="Palette de câbles",
            prix_de_vente=0, duree_de_vie=10, nombre_par_palette=1,
        )
        PrixProduit.objects.create(produit=tubes, fournisseur=fournisseur, prix_achat=1_000)
        PrixProduit.objects.create(produit=cables, fournisseur=fournisseur, prix_achat=3_000)

        stock_tubes = Stock.objects.create(produit=tubes, quantite=2, palettes_max=10)
        stock_cables = Stock.objects.create(produit=cables, quantite=1, palettes_max=10)
        PointDeVente.objects.create(
            nom="PDV tubes", lieu=lieu, heures_de_travail=0, stock=stock_tubes
        )
        PointDeVente.objects.create(
            nom="PDV câbles", lieu=lieu, heures_de_travail=0, stock=stock_cables
        )

        self.assertEqual(Lieu.objects.first().costs(), ATTENDU)