from urllib import request
from django.shortcuts import render
from .models import Produto
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse


class ListaProduto(ListView):
    model = Produto
    template_name= 'lista.html'    
    paginate_by = 6
    context_object_name = 'produtos'
    
   
class DetalheProduto(DetailView):
    model = Produto
    template_name = 'detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    
    
class AdicionarAoCarrinho(ListaProduto):
    pass
    
    
class RemoverDoCarrinho(ListaProduto):
    pass
    
    
class Carrinho(ListaProduto):
    pass
    
    
class Finalizar(ListaProduto):
    pass
    
