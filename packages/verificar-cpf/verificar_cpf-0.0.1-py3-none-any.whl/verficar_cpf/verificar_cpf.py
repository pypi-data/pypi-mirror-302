


# Programa para verificar se um CPF é válido conferindo os dígitos verificadores.


def inserir():

    # Este input vai retirar espaços ou caracters, deixando apenas os números.
    cpf_in=input("Digite seu CPF (apenas os números)\n=> ").replace(".","").replace("-","").replace("_","").replace(" ","")
    cpf_lista=[] # Declarando a variável lista.

    for numero in cpf_in: # Gera uma lista apenas com os números do cpf.
        numero=int(numero)
        if isinstance(numero, int):
            cpf_lista.append(numero)
    return cpf_lista
    

def verificar(cpf_lista):

    # Declaração das variáveis.
    mult=1
    dig_1=0
    dig_2=0
    
    for i in range(9):  # Vai calcular o primeiro dígito verificador
        dig_1+=mult*cpf_lista[i]
        mult+=1
        
    dig_1=dig_1%11
    dig_1=0 if dig_1==10 else dig_1

    if dig_1!= cpf_lista[9]: # Compara o primeiro dígito verificar. Se não for válido, não executa o restante do código.
        return "<< CPF NÃO É VÁLIDO >>"

    else:
        mult=0
        for i in range(10):  # Vai calcular o segundo dígito verificador
            dig_2+=mult*cpf_lista[i]
            mult+=1
        
        dig_2=dig_2%11
        dig_2=0 if dig_2==10 else dig_2

        if dig_2!= cpf_lista[10]:
           return "<< CPF NÃO É VÁLIDO >>"
        else:
            return "== CPF VERIFICADO. OK!!! =="
        
# Usado para testar as funções. Não necessário para o código funcionar.
# cpf_lista = inserir()
#print(verificar(cpf_lista))