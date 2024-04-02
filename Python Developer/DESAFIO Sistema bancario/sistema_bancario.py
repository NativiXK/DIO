
class Transacao:

    def __init__(self, valor : float) -> None:
        self.__valor : float = valor
        self.__tipo : str

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def tipo(self) -> str:
        return self.__tipo
    
    @valor.setter
    def valor(self, valor : float):
        self.__valor = valor

    def __str__(self):
        return f"{self.tipo} - R${self.valor}"

class Saque(Transacao):

    def __init__(self, valor: float) -> None:
        super().__init__(valor)
        self.tipo = self.__class__.__name__

class Deposito(Transacao):

    def __init__(self, valor: float) -> None:
        super().__init__(valor)
        self.tipo = self.__class__.__name__

class Extrato:

    def __init__(self) -> None:
        pass

class Usuario:

    def __init__(self, nome, sobrenome, email) -> None:
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def sobrenome(self) -> str:
        return self.__sobrenome
    
    @property
    def email(self) -> str:
        return self.__email

    @nome.setter
    def nome(self, nome : str):
        self.__nome = nome

    @sobrenome.setter
    def sobrenome(self, sobrenome):
        self.__sobrenome = sobrenome
    
    @email.setter
    def email(self, email):
        self.__email = email

    def __str__(self) -> str:
        return f"Cliente: {self.nome} {self.sobrenome}\t\tEmail: {self.email}"

class Conta:

    LIMITE_SAQUES = 3
    MAX_SAQUE = 500

    def __init__(self, usuario : Usuario, numero : int, senha : int, saldo : float = 0) -> None:
        self.__usuario : Usuario = usuario
        self.__numero : int = numero
        self.__senha : int = senha
        self.__saldo : float = saldo
        self.__saques : int = 0
        self.__extrato : Extrato = Extrato()

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def senha(self) -> int:
        return self.__senha

    @property
    def extrato(self):
        extrato = "\nEXTRATO:\n"
        extrato += ("-" * 20)
        extrato += f"\n{self.__usuario}\n"
        extrato += ("-" * 20)
        extrato += f"\nConta: {self.__numero}\n"
        extrato += ("-" * 20)
        extrato += '\n' + self.__extrato

    def depositar(self, valor : float) -> None:

        assert((type(valor) in (float, int)) and (valor > 0))

        self.__saldo += valor
        self.__extrato += f"\nDepósito de R${valor:.2f}"

        print(f"Depósito de R${valor:.2f} efetuado.")

    def sacar(self, valor : float) -> None:
       
        assert((type(valor) in (float, int)) and (valor > 0))

        if (valor > Conta.MAX_SAQUE):
            print(f"Valor de saque máximo excedeu o limite de R${Conta.MAX_SAQUE:.2f}!")
            return

        if (self.__saldo <= 0):
            print("Saldo insuficiente")
            return

        if (self.__saques >= Conta.LIMITE_SAQUES):
            print(f"Limite de {Conta.LIMITE_SAQUES} saques diários atingido")
            return
        
        self.__saldo -= valor
        self.__extrato += f"\nSaque de R${valor:.2f}"
        self.__saques += 1

        print(f"Saque de R${valor:.2f} efetuado.")

    def __str__(self) -> str:
        return f"Conta: {self.__numero}\nSaldo: R${self.__saldo}\n\nLimite de saque: R${Conta.MAX_SAQUE}\nSaques disponíveis: {Conta.LIMITE_SAQUES - self.__saques}"

    @staticmethod
    def nova_conta() -> 'Conta':
        print('CRIANDO NOVA CONTA')
        print('-' * 20)
        nome = input("Nome: ")
        sobrenome = input('Sobrenome: ')
        email = input('Email: ')

        nova_senha = hash(input('Senha: '))
        conf_senha = hash(input('Confirme a senha: '))

        if nova_senha != conf_senha:
            print('As senhas não são compatíveis!')
            return None

        usuario = Usuario(nome, sobrenome, email)

        return Conta(usuario=usuario, numero=hash(usuario), senha=nova_senha)

def menu(conta : Conta) -> str:
    menu = f"""
------------------------
        CONTA

{str(conta) if conta is not None else "Nenhuma conta selecionada!"}

------------------------
        MENU

Digite a opção desejada:

[D] - Depósitar
[S] - Sacar
[E] - Extrato

[NC] - Nova conta
[SC] - Selecionar conta

[F] - Sair

Opção: """
    return input(menu).upper()

if __name__ == "__main__":

    contas = []

    conta_selecionada : Conta = None

    while True:
        
        acao = menu(conta_selecionada)
        print()

        if acao == 'F':
            break

        if acao == 'D':
            print('Depósito:')
            valor = int(input("Insira o valor: R$"))
            conta_selecionada.depositar(valor)
            input()

        if acao == 'S':
            print('Saque:')
            valor = int(input("Insira o valor: R$"))
            conta_selecionada.sacar(valor)
            input()

        if acao == 'E':
            conta_selecionada.extrato()
            input()

        if acao == 'NC':
            nova_conta = Conta.nova_conta()

            if nova_conta is not None:
                print('-' * 20)
                print(nova_conta)
                confirma = input('\nDeseja criar esta conta? [S/N]').upper()
                if confirma == 'S':
                    contas.append(nova_conta)
                    print('Conta criada!')
                else:
                    print('A conta não foi criada!')
                
                conta_selecionada = nova_conta
            else:
                print('Não foi possível criar uma nova conta.')
                input()

        if acao == 'SC':
            print('CONTAS')
            print('-' * 20)
            for conta in contas:
                print(' - ' + str(conta.numero))
            print('-' * 20)
            print('SELECIONAR CONTA')
            print('-' * 20)

            try:
                numero = int(input('Número: '))
                senha = hash(input('Senha: '))

            except Exception:
                numero = 0
                senha = 0

            conta_numero = None

            for conta in contas:
                if (conta.numero == numero):
                    if (conta.senha == senha):
                        conta_numero = conta
                        break
                    else:
                        print('Senha inválida')
                        conta_numero = Conta
                        input()

            if conta_numero is not None:
                conta_selecionada = conta_numero
            else:
                print('Nenhuma conta localizada!')
                input()

            print('-' * 20)
