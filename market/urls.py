from django.urls import path, include
from django.views.generic import TemplateView, ListView

from . import views

urlpatterns = [
	path('', views.home, name="acceuil"),
	path('test', views.test),
	path('produits', views.products, name="catalogue"),
	path('produit/<int:id>', views.detail, name="produit"),
	path('cart', views.my_cart, name="cart"),

	path('login/', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register_view, name='register'),
	path('about', TemplateView.as_view(template_name="market/about.html"), name="about"),
	path('contact', TemplateView.as_view(template_name="market/contact.html"), name="contact"),
	# path('add/', views.new_image, name="new_img"),

		#******************************#
		#***********AJAX URLs**********#
		#******************************#
	path('total/<int:id>', views.get_total, name="total"),
	path('price/<int:id>/<operateur>', views.get_price, name="price"),
	path('delete/<int:id>', views.delete_cmd, name="delete"),
	path('produit/<int:id>/add', views.add_product_in_card, name="ajouter"),
	path('details', views.product_details, name="details"),
	path('totaux', views.get_totaux, name=""),
	path('set_cmd_state', views.set_cmd_state, name="set_cmd_state"),
]