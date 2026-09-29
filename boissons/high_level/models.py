# Create your models here.
from django.db import models


# ========== MODÈLES DE BASE PAYS & VILLE ==========

class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.IntegerField()
    tarif_electrique = models.IntegerField()
    salaire_minimum = models.IntegerField()

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Pays"


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    taxe_immobiliere = models.IntegerField()
    prix_m2 = models.IntegerField()
    pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return self.nom


# ========== MODÈLES MACHINE ==========

class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    duree_de_vie = models.IntegerField()
    cout_maintenance = models.IntegerField()
    superficie = models.IntegerField()

    def __str__(self):
        return self.nom


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
        related_name="+",
    )
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.machine.nom}"

    class Meta:
        verbose_name_plural = "QuantiteMachines"


# ========== MODÈLES LIEU ==========

class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
        related_name="+",
    )
    superficie = models.IntegerField()
    machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.IntegerField()

    def __str__(self):
        return self.nom


# ========== MODÈLES PRODUIT ==========

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()

    def __str__(self):
        return self.nom


# ========== MODÈLE ABSTRAIT QUANTITE ==========

class QuantiteProduitBase(models.Model):
    quantite = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"


# ========== MODÈLES QUANTITÉ DE PRODUITS ==========

class Stock(QuantiteProduitBase):
    palettes_max = models.IntegerField()

    def __str__(self):
        return f"Stock: {self.quantite} x {self.produit.nom}"


# ========== MODÈLES OPÉRATION ==========

class Operation(models.Model):
    nom = models.CharField(max_length=100)
    operation_suivante = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    cout = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
        related_name="+",
    )
    quantite_produits = models.IntegerField()
    heures_de_travail = models.IntegerField()
    consommation_electrique = models.IntegerField()

    def __str__(self):
        return self.nom


# ========== MODÈLES TRANSPORT ==========

class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.IntegerField()
    delai = models.IntegerField()
    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="+",
    )
    arrivee = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return f"{self.depart.nom} → {self.arrivee.nom}"


# ========== MODÈLES VENTE ==========

class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="+",
    )
    heures_de_travail = models.IntegerField()
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return self.nom


# ========== MODÈLES FOURNISSEUR ==========

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class PrixProduit(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name="+",
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name="+",
    )
    prix_achat = models.IntegerField()

    def __str__(self):
        return f"{self.produit.nom} - {self.fournisseur.nom}"

    class Meta:
        unique_together = ('produit', 'fournisseur')


# ========== MODÈLES FACTURE ==========

class Facture(models.Model):
    quantite_produits = models.IntegerField()
    reduction = models.IntegerField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
        related_name="+",
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return f"Facture {self.id} - {self.point_de_vente.nom}"