from django.shortcuts import render, redirect, get_object_or_404
from perfil.models import PerfilUsuario
from .models import Produto, Variacao
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

from pprint import pprint


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
        produto = variacao.produto
        variacao_estoque = variacao.estoque
        
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
        imagem = imagem.name
        
        
        # VERIFICADO ESTOQUE
        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insulficiente.')
            return redirect(http_referer)
        
        # CRIANDO SESSION
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
        
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if variacao_estoque < quantidade_carrinho:
                messages.error(self.request, f'Desculpe. Só temos {variacao_estoque} em estoque.')
                quantidade_carrinho = variacao_estoque
                return redirect(http_referer)         
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
            
        else:
            carrinho[variacao_id] = {
                'produto_id' : produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome' : variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade' : quantidade,
                'slug' : slug,
                'imagem' : imagem,
            }
            
        self.request.session.save()       
        
        # TODO: falha ao adicionar mensagem de adicionar ao carrinho
        messages.success(self.request,
                         f'{produto_nome} {variacao_nome} '
                         f'foi adicionado com sucesso {quantidade}x.')
        return redirect(http_referer)
    
    
class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER')
        variacao_id = self.request.GET.get('vid')
         
        if not variacao_id:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer) 
        
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        
        carrinho = self.request.session['carrinho'][variacao_id]
        
        messages.success(self.request, 
                         f'O Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} foi removido com sucesso.')
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        
        return redirect(http_referer)
    
    
class Carrinho(ListaProduto):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')
        return render(self.request, 'carrinho.html', {'carrinho': carrinho})
    
    
class ResumoDaCompra(ListaProduto):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        perfil = PerfilUsuario.objects.filter(usuario= self.request.user).exists()
        
        if not perfil:
            messages.error(self.request, 'Informações incompletas, por favor atualizar cadastro.')
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Não existe itens no seu carrinho de compras.')
            return redirect('produto:lista')
        
        contexto ={
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }
        # TODO: falta enviar os dados do usuário no html
        
        return render(self.request, 'resumodacompra.html', contexto)
    
