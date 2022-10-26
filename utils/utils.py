def estilo_moeda(valor):
    return f'R$ {valor:.2f}'.replace('.',',')


def cart_total_quant(carrinho):    
    quant_total = sum([item['quantidade'] for item in carrinho.values()])
    return quant_total



def cart_total_preco(carrinho):
    total_preco = sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item 
            in carrinho.values()
        ]
    )
    return round(total_preco, 2)
    