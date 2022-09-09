def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])