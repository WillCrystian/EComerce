from django import template
from utils import utils

register = template.Library()

@register.filter(name='estilo_moeda')
def estilo_moeda(valor):
    return utils.estilo_moeda(valor)

@register.filter
def cart_total_quant(carrinho):
    return utils.cart_total_quant(carrinho)

@register.filter
def cart_total_preco(carrinho):
    return utils.cart_total_preco(carrinho)
