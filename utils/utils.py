def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_totals(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )

def formata_cpf(cpf):
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def formata_cep(cep):
    return f'{cep[:5]}-{cep[5:]}'