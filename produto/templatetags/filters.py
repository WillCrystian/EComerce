from django import template

register = template.Library()

@register.filter(name='estilo_moeda')
def estilo_moeda(valor):
    return f'R$ {valor:.2f}'.replace('.',',')