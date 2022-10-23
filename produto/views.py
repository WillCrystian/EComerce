from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Variacao
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse


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
    
    
class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # retornar a página para anterior
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        # obter o valor do vid da url
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id= variacao_id)
        
        # CRIANDO SESSION
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
        
        if variacao_id in carrinho:
            # TODO: variacao existe
            pass
        else:
            # TODO: variacao não existe
            pass
            
            
        return HttpResponse(f'{variacao.produto} {variacao.nome}')
       
        return redirect(http_referer)
    
    
class RemoverDoCarrinho(ListaProduto):
    pass
    
    
class Carrinho(ListaProduto):
    pass
    
    
class Finalizar(ListaProduto):
    pass
    
