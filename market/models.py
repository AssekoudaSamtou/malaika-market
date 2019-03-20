from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Image(models.Model):
	photo = models.ImageField(upload_to="photos/")

	class Meta:
		verbose_name = "Image"

	def __str__(self):
		return self.photo.url


class Produit(models.Model):
	libelle = models.CharField(max_length=100)
	marque = models.CharField(max_length=42)
	prix = models.DecimalField(null=True, max_digits=7, decimal_places=2)
	description = models.TextField(null=True)
	nb_visite = models.IntegerField(null=True)
	logo = models.OneToOneField(Image, unique=True, related_name="+", on_delete=models.CASCADE, verbose_name="Image Principale")
	images = models.ManyToManyField(Image, through='ProduitImage', related_name='+')
	date_ajout = models.DateTimeField(default=timezone.now, verbose_name="Date d'ajout")
	publie_le = models.DateTimeField(null=True, verbose_name="Publié Le")
	categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
	is_visible = models.BooleanField(verbose_name="Produit publié ?", default=True)

	class Meta:
		verbose_name = "Produit"
		ordering = ['publie_le']

	def __str__(self):
		return self.libelle

class Client(User):
	telephone = models.CharField(max_length=100)
	lieux_livraison = models.CharField(max_length=200)
	panier = models.ManyToManyField(Produit, through='Commande', related_name='+', verbose_name="Commandes")

	class Meta:
		verbose_name = "Client"

	def __str__(self):
		return self.username

	def get_commande_total(self):
		commandes = Commande.objects.filter(client=self, est_paye=False, est_suppr=False)
		return sum([cmd.total for cmd in commandes])

class ProduitImage(models.Model):
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Produit  avec des images"
		ordering = ['produit']

	def __str__(self):
		return f"{self.image.photo.url} appartient à {self.produit.libelle}"


class Categorie(models.Model):
	nom = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Categorie Produit"

	def __str__(self):
		return self.nom

class Commande(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	quantite = models.IntegerField(null=True, default=1)
	est_paye = models.BooleanField(verbose_name="Commande payée ?", default=False)
	est_suppr = models.BooleanField(verbose_name="Commande supprimée ?", default=False)
	total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
	taxe_sur_livraison = models.DecimalField(default=0, max_digits=7, decimal_places=2)
	pret_a_payer = models.BooleanField(verbose_name="Commande prete à payer ?", default=True)

	def __str__(self):
		return f"{self.client.username} à commandé {self.produit.libelle}"