from django import template

register = template.Library()
# print("test filtre")

@register.filter
def item(value, arg):
	return value[arg]

@register.filter
def sous_total(value):
	return sum([cmd.total for cmd in value if cmd.pret_a_payer])

@register.filter
def taxe_total(value):
	return sum([cmd.taxe_sur_livraison for cmd in value if cmd.pret_a_payer])

@register.filter
def totaux(value):
	return sous_total(value) + taxe_total(value)