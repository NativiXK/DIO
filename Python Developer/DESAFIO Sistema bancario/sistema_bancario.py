operacoes = []
saldo = 0
saques = 0
LIMITE_SAQUES = 3
MAX_SAQUE = 500

def depositar(valor : float) -> None:
    global saldo
    global operacoes

    assert((type(valor) in (float, int)) and (valor > 0))

    saldo += valor
    operacoes.append(valor)
    print(f"Depósito de R${valor:.2f} efetuado.")

def sacar(valor : float) -> None:
    global saldo
    global saques
    global operacoes
    
    assert((type(valor) in (float, int)) and (valor > 0))

    if (valor > MAX_SAQUE):
        print(f"Valor de saque máximo excedeu o limite de R${MAX_SAQUE:.2f}!")
        return

    if (saldo <= 0):
        print("Saldo insuficiente")
        return

    if (saques >= LIMITE_SAQUES):
        print(f"Limite de {LIMITE_SAQUES} saques diários atingido")
        return
    
    saldo -= valor
    operacoes.append(-valor)
    saques += 1

    print(f"Saque de R${valor:.2f} efetuado.")

def extrato():
    global operacoes

    print("\nEXTRATO:")
    if len(operacoes) == 0:
        print("Nenhuma operação efetuada")
        return
    
    for op in operacoes:
        if (op > 0):
            print(f"Depósito:  R${op:.2f}")
        if (op < 0):
            print(f"Saque:  R${op:.2f}")            

if __name__ == "__main__":
    
    while True:
        menu = f"""
Saldo: R${saldo}

Digite a opção desejada:

[1] - Depósitar
[2] - Sacar
[E] - Extrato

[0] - Sair

"""

        acao = input(menu).upper()
        print()

        if acao == '0':
            break

        if acao == '1':
            print('Depósito:')
            valor = int(input("Insira o valor: R$"))
            depositar(valor)
        
        if acao == '2':
            print('Saque:')
            valor = int(input("Insira o valor: R$"))
            sacar(valor)

        if acao == 'E':
            extrato()
