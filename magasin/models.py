# magasin/models.py

from django.db import models
from datetime import date

TYPE_CHOICES = [
    ('em', 'emballé'),
    ('fr', 'Frais'),
    ('cs', 'Conserve')
]

class Categorie(models.Model):
    TYPE_CHOICES_CAT = [
        ('Alimentaire', 'Alimentaire'),
        ('Meuble', 'Meuble'),
        ('Sanitaire', 'Sanitaire'),
        ('Vaisselle', 'Vaisselle'),
        ('Vetement', 'Vêtement'),
        ('Jouets', 'Jouets'),
        ('Linge', 'Linge de Maison'),
        ('Bijoux', 'Bijoux'),
        ('Decor', 'Décor'),
    ]
    
    name = models.CharField(
        max_length=50, 
        choices=TYPE_CHOICES_CAT, 
        default='Alimentaire'
    )
    
    def __str__(self):
        return self.name


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)
    
    def __str__(self):
        return self.nom


class Produit(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField(default='Non définie')
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    img = models.ImageField(upload_to='media/', blank=True, null=True)
    
    categorie = models.ForeignKey(
        Categorie, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    fournisseur = models.ForeignKey(
        Fournisseur, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"{self.libelle} - {self.prix}"


class ProduitNC(Produit):
    duree_garantie = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.libelle} (NC) - {self.duree_garantie}"


class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        editable=True, 
        default=0
    )
    produits = models.ManyToManyField(Produit)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.totalCde = sum(p.prix for p in self.produits.all())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Commande du {self.dateCde} - {self.totalCde}"