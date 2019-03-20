from django.contrib import admin
# import xadmin
from .models import *

# Register your models here.

admin.site.register(Image)
admin.site.register(Produit)
admin.site.register(ProduitImage)
admin.site.register(Categorie)
admin.site.register(Client)
admin.site.register(Commande)