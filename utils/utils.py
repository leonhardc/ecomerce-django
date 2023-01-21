from datetime import date

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

def valida_cpf(cpf):
    
    cpf = str(cpf)
    cpf_list = list(cpf[:-2])
    
    for _ in range(2): # Gera os dois ultimos digitos do cpf
        range_list = list(range(len(cpf_list)+1, 1, -1))
        total = 0
        
        for dig, mul in zip(cpf_list, range_list):
            total += int(dig) * mul
        digito = 11-(total % 11) # usado para validar qual será o digito do cpf

        if digito > 9: # Se o valor calculado para o digito for maior que 9, muda o digito para 0.                         
            digito = 0 
        
        cpf_list.append(str(digito))

    novo_cpf = "".join(cpf_list)

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Sequencias geram verdadeiro, o que não é válido no nosso caso.
    if cpf == novo_cpf and not sequencia:
        # cpf válido
        return True
    else:
        # cpf invalido
        return False

def calcula_idade(nascimento): 
    hoje = date.today() 
    diff = hoje - nascimento 
    idade = int(diff.days/365)
    return idade

def formata_data(data):
    # Formato da Data:Entrada: dia/mes/ano
    # Formato da Data:Saida: ano-mes-dia
    if data:
        list_data = str.split(data, '/')
        dia, mes, ano = list_data
        return f'{ano}-{mes}-{dia}'
    else:
        return "1900-01-01"


def formata_descricao(descricao):
    if len(descricao) > 50:
        descricao = descricao[:50] + '...'
        return descricao
    else:
        return descricao

