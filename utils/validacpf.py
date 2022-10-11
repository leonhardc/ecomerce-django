
def valida_cpf(cpf):
    cpf = str(cpf)
    cpf_list = list(cpf[:-2])

    for _ in range(2): 
        range_list = list(range(len(cpf_list)+1, 1, -1))
        total = 0
        # gerando primeiro digito
        for dig, mul in zip(cpf_list, range_list):
            total += int(dig) * mul
        digito = 11-(total % 11) # usado para validar qual será o digito do cpf
        
        if digito > 9: # Se o valor calculado para o digito for maior que 9, 
                        #muda o digito para 0. 
            digito = 0 
        
        cpf_list.append(str(digito))

    novo_cpf = "".join(cpf_list)

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        # cpf válido
        return True
    else:
        # cpf invalido
        return False
