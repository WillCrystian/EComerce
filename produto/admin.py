from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1
    list_display= ('id','nome', 'produto', 'preco', 'preco_promocional', 'estoque')

    
class ProdutoAdmin(admin.ModelAdmin):
    list_display= ('id','nome', 'preco_marketing', 'preco_marketing_promocional', 'slug', 'tipo')
    list_display_links= ('id', 'nome', 'preco_marketing')
    inlines = [VariacaoInline]   
    
admin.site.register(Produto, ProdutoAdmin)    
admin.site.register(Variacao)