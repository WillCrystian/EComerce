from django.shortcuts import render, redirect   
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from .models import ItemPedido, Pedido
from django.urls import reverse


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        return super().dispatch(*args, **kwargs)
    
        # verificando se o pedido é do usuário que está ligado
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario= self.request.user)
        return qs
    

class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'
    


    
class SalvarPedido(View):
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer login.')
            return redirect('perfil:criar')
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carinho está vázio.')
            return redirect('produto:lista')
 
        carrinho = self.request.session.get('carrinho')
        # pegar as variacoes que estão no carrinho
        carrinho_variacoes_ids = [v for v in carrinho]
        
        # pegar TODAS (id__in=) as varições que estão no banco de dados
        bd_variacoes = list(Variacao.objects.select_related('produto').filter(id__in= carrinho_variacoes_ids))
       
        for varicao in bd_variacoes:
            vid = str(varicao.id)
            nome = varicao.nome
            estoque = varicao.estoque
            preco_unit = varicao.preco
            preco_unit_promo = varicao.preco_promocional
            
            
            if estoque < carrinho[vid]['quantidade']:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unit
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unit_promo
                self.request.session.save()
                messages.warning(self.request,
                                 f'Estoque do produto {varicao.produto} {nome} insulficiente para quantidade do seu carrinho')
                return redirect('produto:carrinho')
            
        qtd_total_carrinho = utils.cart_total_quant(carrinho)
        valor_total_carrinho = utils.cart_total_preco(carrinho)
                
        pedido = Pedido(
            usuario= self.request.user,
            total = valor_total_carrinho,
            qtd_total= qtd_total_carrinho,
            status= 'C',
        )
        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                        pedido = pedido,
                        produto = v['produto_nome'],
                        produto_id = v['produto_id'],
                        variacao = v['variacao_nome'],
                        variacao_id = v['variacao_id'],
                        preco = v['preco_quantitativo'],
                        preco_promocional = v['preco_quantitativo_promocional'],
                        quantidade = v['quantidade'],
                        imagem = v['imagem'],
                ) for v in carrinho.values()
            ]
        )
        
        
        del self.request.session['carrinho']
        
        return redirect(
            reverse('pedido:pagar', kwargs={'pk': pedido.pk})
            )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'detalhe_pedido.html'
    ordering = ['-id']


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 6
    template_name = 'lista_pedidos.html'
    ordering = ['-id']