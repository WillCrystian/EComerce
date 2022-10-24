def cart_total_quant(carrinho):    
    quant_total = sum([item['quantidade'] for item in carrinho.values()])
    return quant_total

def estilo_moeda(valor):
    return f'R$ {valor:.2f}'.replace('.',',')