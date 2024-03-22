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
    print(f"Depósito de R${valor} efetuado.\nSaldo atual: R${saldo}")

def sacar(valor : float) -> None:
    global saldo
    global saques
    global operacoes
    
    assert((type(valor) in (float, int)) and (valor > 0))

    if (valor > MAX_SAQUE):
        print(f"Valor de saque máximo excedeu o limite de R${MAX_SAQUE}!")
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

    print(f"Saque de R${valor} efetuado.\nSaldo atual: R${saldo}")

def extrato():
    global operacoes

    print("\n\nEXTRATO:")
    for op in operacoes:
        if (op > 0):
            print(f"Depósito:  R${op}.")
        if (op < 0):
            print(f"Saque:  R${op}.")            

if __name__ == "__main__":
    sacar(100)
    depositar(500.5)
    depositar(250)
    sacar(300)
    sacar(200)
    depositar(500)
    sacar(600)
    sacar(400)
    sacar(350)
    extrato()