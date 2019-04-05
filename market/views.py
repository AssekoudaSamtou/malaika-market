from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Image, Produit, Client, Commande
from .forms import NewImageForm, LoginForm, RegisterForm

from market.templatetags import my_filters
import time
# return HttpResponseRedirect('/success/url/')

def home(request):
	# for m in request.META : print(m, " : ", request.META[m])
	# print(request.session)
	return render(request, "market/acceuil.html")

def products(request):
	# time.sleep(3)
	# input("En pause")
	if request.method == "GET":
		if request.user.is_authenticated:
			client = Client.objects.get(id=request.user.id)
			# cmd = client.panier.all()
			cmd = Commande.objects.filter(client=client, est_paye=False, est_suppr=False)
			cmd = [c.produit for c in cmd]
		else:
			cmd = []

		if request.is_ajax():
			name = request.GET.get("name")
			produits = Produit.objects.filter(libelle__contains=name)
		else:
			produits = Produit.objects.all()

		in_cart = {}
		for pro in produits:
			if pro in cmd:
				in_cart[pro] = True
			else:
				in_cart[pro] = False

		in_cart["samtou"] = "Test success"
		# print(cmd)
		# print(in_cart)
		context = {'produits': produits, 'in_cart': in_cart}
		if request.is_ajax():
			return render(request, "market/produits_avec_ajax.html", context)
			
		return render(request, "market/produits.html", context)

def login_view(request):
	form = LoginForm(request.POST or None)
	context = {"form" : form}
	# print(request.user.is_authenticated)
	if form.is_valid():
		# print(form.cleaned_data)
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(request, username=username, password=password)
		# print(request.user.is_authenticated)
		if user is not None:
			login(request, user)
			print(request.user.is_authenticated)
			# context['form'] = LoginForm()
			return redirect("/")
		else:
			# print("Error")
			pass

	return render(request, "auth/login.html", context)

def logout_view(request):
	logout(request)
	return redirect("/")

def register_view(request):
	form = RegisterForm(request.POST or None)
	context = {"form" : form}
	if form.is_valid():
		# print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = Client.objects.create_user(username, email, password)
		# print(new_user)

	return render(request, "auth/register.html", context)

def detail(request, id):
	images = get_object_or_404(Produit, id=id).images.all()
	produit = get_object_or_404(Produit, id=id)

	context = {'images': images, 'produit':produit}
	return render(request, "market/details.html", context)

@login_required
def new_image(request):
	sauvegarde = False
	form = NewImageForm(request.POST or None, request.FILES)
	print("YES")
	if form.is_valid():
		img = Image()
		img.photo = form.cleaned_data["photo"]
		img.save()
		sauvegarde = True

	context = {'form': form, 'sauvegarde': sauvegarde}
	return render(request, 'market/add_img.html', context)

@login_required
def my_cart(request):
	client = Client.objects.get(id=request.user.id)
	# print("SAM", client.get_commande_total())
	cmd = Commande.objects.filter(client=client, est_paye=False, est_suppr=False).order_by("-produit")
	context = {
		"commandes" : cmd,
		"total"     : None,
	}
	return render(request, "market/cart.html", context)

"""
	Les vues pour les requetes AJAX
"""
@login_required
def get_total(request, id):
	if request.is_ajax():
		# print(id)
		client = Client.objects.get(id=request.user.id)
		cmd = get_object_or_404(Commande, id=id)
		# print(cmd.total)
		return HttpResponse(f"{cmd.total}")
	else:
		raise Http404

@login_required
def get_price(request, id, operateur):
	if request.is_ajax():
		# print(operateur)
		p = get_object_or_404(Produit, id=id)
		prix = p.prix

		client = Client.objects.get(id=request.user.id)
		cmd = get_object_or_404(Commande, client=client, produit=p, est_paye=False, est_suppr=False)
		# print(cmd)
		if operateur == "+" : cmd.quantite += 1
		if operateur == "-" : cmd.quantite -= 1

		cmd.total = prix * cmd.quantite
		cmd.save()
		# data = {"1": prix}
		# print(JsonResponse(data))
		return HttpResponse(f"{prix}")
	else:
		raise Http404

@login_required
def delete_cmd(request, id):
	if request.is_ajax():
		cmd = get_object_or_404(Commande, id=id)
		cmd.est_suppr = True
		cmd.save()
		return HttpResponse(f"YES")
	else:
		raise Http404

@login_required
def add_product_in_card(request, id):
	if request.is_ajax():
		# print("YES")
		client = get_object_or_404(Client, id=request.user.id)
		produit = get_object_or_404(Produit, id=id)
		cmd = Commande(produit=produit, client=client, total=produit.prix)
		cmd.save()
		return HttpResponse(f"YES")
	else:
		raise Http404


def test(request):
	
	return JsonResponse({"ip":"192.168.1.1", "pays":"TOGO"})

def product_details(request):
	if request.is_ajax():
		if request.method == "GET":
			pk = request.GET.get("id")
			images = get_object_or_404(Produit, id=int(pk)).images.all()
			i=1; context = {}
			for img in images:
				context[str(i)] = img.photo.url
				i += 1
			# print(context)
			return JsonResponse(context)

def get_totaux(request):
	if request.is_ajax() and request.method ==  "GET":
		
		client = Client.objects.get(id=request.user.id) # on recupere le cilent connecté
		cmds = Commande.objects.filter(client=client, est_paye=False, est_suppr=False, pret_a_payer=True).order_by("-produit")

		context = {}
		
		context["sous_total"] = my_filters.sous_total(cmds)
		context["taxe_total"] = my_filters.taxe_total(cmds)
		context["totaux"] = context["sous_total"] + context["taxe_total"]

		return JsonResponse(context)

def set_cmd_state(request):
	if request.is_ajax() and request.method ==  "GET":

		client = Client.objects.get(id=request.user.id)

		pk = request.GET.get("pk").split("commande")[1]
		attr = request.GET.get("attribute")
		state = request.GET.get("state")
		cmd = Commande.objects.get(id=int(pk))

		if (attr == "pret_a_payer"):
			print(cmd)
			print(cmd.pret_a_payer)
			cmd.pret_a_payer = bool(int(state))
			cmd.save()
			print(cmd.pret_a_payer)

		return HttpResponse(f"YES")