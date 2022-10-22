def validar_cpf(cpf):
    cpf = str(cpf)
    cpf = cpf.replace('.','').replace('-','')

    novo_cpf = cpf[0:9]
    mult = 10
    soma = 0

    for digito in novo_cpf:
        soma = soma + (int(digito) * mult)
        mult -= 1

    primeiro_digito = 11 - (soma % 11)

    if primeiro_digito > 9:
        primeiro_digito = 0
        
    novo_cpf = str(novo_cpf) + str(primeiro_digito)    
    mult2 = 11
    soma2 = 0

    for valor in novo_cpf:
        soma2 = soma2 + (int(valor) * mult2)
        mult2 -= 1
        
    segundo_digito = 11 - (soma2 % 11)

    if segundo_digito > 9:
        segundo_digito = 0
        
    novo_cpf = novo_cpf + str(segundo_digito)

    if novo_cpf == cpf:
        return True
    else:
        return False