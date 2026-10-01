from django.db import models

class JsonMixin:
    def json(self):
        data = {"id": self.pk, "type": self.__class__.__name__}
        for field in self._meta.concrete_fields:
            if field.name == "id":
                continue
            data[field.name] = getattr(self, field.attname)
        for field in self._meta.many_to_many:
            data[field.name] = list(
                getattr(self, field.name).values_list("pk", flat=True)
            )
        return data

    def json_extended(self):
        data = self.json()
        for field in self._meta.concrete_fields:
            if field.many_to_one:
                related = getattr(self, field.name)
                data[field.name] = related.json_extended() if related else None
        for field in self._meta.many_to_many:
            data[field.name] = [
                o.json_extended() for o in getattr(self, field.name).all()
            ]
        return data


# ========== MODÈLES DE BASE PAYS & VILLE ==========

class Pays(JsonMixin, models.Model):
    nom = models.CharField(max_length=100)
    tva = models.IntegerField()
    tarif_electrique = models.IntegerField()
    salaire_minimum = models.IntegerField()

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Pays"


class Ville(JsonMixin, models.Model):
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

    def costs(self):
        return sum(lieu.costs() for lieu in self.lieu_set.all())


# ========== MODÈLES MACHINE ==========

class Machine(JsonMixin, models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    duree_de_vie = models.IntegerField()
    cout_maintenance = models.IntegerField()
    superficie = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        return self.prix


class QuantiteMachine(JsonMixin, models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
        related_name="+",
    )
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.machine.nom}"

    def costs(self):
        return self.nombre * self.machine.costs()

    class Meta:
        verbose_name_plural = "QuantiteMachines"


# ========== MODÈLES LIEU ==========

class Lieu(JsonMixin, models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.IntegerField()
    machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        terrain = self.superficie * self.ville.prix_m2
        electricite = (
            self.consommation_electrique * self.ville.pays.tarif_electrique // 100
        )
        machines = sum(q.costs() for q in self.machines.all())
        ventes = sum(p.costs() for p in PointDeVente.objects.filter(lieu=self))
        return terrain + electricite + machines + ventes


# ========== MODÈLES PRODUIT ==========

class Produit(JsonMixin, models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        prix = PrixProduit.objects.filter(produit=self).order_by("prix_achat").first()
        return prix.prix_achat if prix else 0


# ========== MODÈLE ABSTRAIT QUANTITE ==========

class QuantiteProduitBase(JsonMixin, models.Model):
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

    def costs(self):
        return self.quantite * self.produit.costs()


# ========== MODÈLES QUANTITÉ DE PRODUITS ==========

class Stock(QuantiteProduitBase):
    palettes_max = models.IntegerField()

    def __str__(self):
        return f"Stock: {self.quantite} x {self.produit.nom}"


# ========== MODÈLES OPÉRATION ==========

class Operation(JsonMixin, models.Model):
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

    def costs(self):
        return self.cout


# ========== MODÈLES TRANSPORT ==========

class Transport(JsonMixin, models.Model):
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

    def costs(self):
        return self.cout


# ========== MODÈLES VENTE ==========

class PointDeVente(JsonMixin, models.Model):
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

    def costs(self):
        salaire = self.heures_de_travail * self.lieu.ville.pays.salaire_minimum
        return self.stock.costs() + salaire


# ========== MODÈLES FOURNISSEUR ==========

class Fournisseur(JsonMixin, models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class PrixProduit(JsonMixin, models.Model):
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

class Facture(JsonMixin, models.Model):
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