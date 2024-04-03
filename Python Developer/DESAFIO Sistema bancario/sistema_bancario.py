"""
Desafio Sistema bancário - Trilha Python Developer - DIO

Mateus Konkol

"""

class Transacao:
    """
    Esta classe serve como base para todas as transações realizadas na conta
    """
    def __init__(self, valor : float, tipo : str) -> None:
        self.__valor : float = valor
        self.__tipo : str = tipo

    @property
    def valor(self) -> float:
        """Retorna o valor da transação"""
        return self.__valor

    @property
    def tipo(self) -> str:
        """Retorna o tipo da transação"""
        return self.__tipo

    @valor.setter
    def valor(self, valor : float):
        self.__valor = valor

    def __str__(self):
        return f"{self.tipo} - R${self.valor}"

class Saque(Transacao):
    """Classe que determina a transação como Saque"""
    def __init__(self, valor: float) -> None:
        super().__init__(valor, "Saque")

class Deposito(Transacao):
    """Classe que determina a transação como depósito"""
    def __init__(self, valor: float) -> None:
        super().__init__(valor, "Depósito")

class Extrato:
    """Classe Extrato armazena e gerencia todas as transações realizadas"""
    def __init__(self) -> None:
        self.__transacoes = []

    def nova_transacao(self, transacao : Transacao):
        """Registra uma nova transação"""
        self.__transacoes.append(transacao)

    def __str__(self) -> str:
        """Retorna uma string com todas as transações formatadas"""
        res = ""

        for trans in self.__transacoes:
            res += f'{str(trans)}\n'
        
        return res

class Usuario:
    """A classe usuário é responsável por gerenciar um usuário que pode ter várias contas"""
    def __init__(self, nome, sobrenome, email) -> None:
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email

    @property
    def nome(self) -> str:
        """Retorna o nome do usuário"""
        return self.__nome

    @property
    def sobrenome(self) -> str:
        """Retorna o sobrenome do usuário"""
        return self.__sobrenome

    @property
    def email(self) -> str:
        """Retorna o email do usuário"""
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
    """A classe conta gerencia todas as transações do usuário assim como as informações da conta"""

    LIMITE_SAQUES : int = 3
    MAX_SAQUE : int = 500

    def __init__(self, usuario : Usuario, numero : int, senha : int, saldo : float = 0) -> None:
        self.__usuario : Usuario = usuario
        self.__numero : int = numero
        self.__senha : int = senha
        self.__saldo : float = saldo
        self.__saques : int = 0
        self.__extrato : Extrato = Extrato()

    @property
    def numero(self) -> int:
        """Retorna o número da conta"""
        return self.__numero

    @property
    def senha(self) -> int:
        """Retorna o hash da senha da conta"""
        return self.__senha

    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta"""
        return self.__saldo

    @property
    def extrato(self):
        """Retorna uma string formatada com as informações da conta e 
        todas as transações realizadas"""
        extrato = "\nEXTRATO:\n"
        extrato += ("-" * 20)
        extrato += f"\n{self.__usuario}\n"
        extrato += ("-" * 20)
        extrato += f"\nConta: {self.__numero}\n"
        extrato += ("-" * 20)
        extrato += '\n' + str(self.__extrato)
        
        return extrato

    def depositar(self, transacao : Deposito) -> None:
        """Realiza um depósito na conta"""

        assert((isinstance(transacao, Deposito)) and (transacao.valor > 0))

        self.__saldo += transacao.valor
        self.__extrato.nova_transacao(transacao=transacao)

        print(f"Depósito de R${transacao.valor:.2f} efetuado.")

    def sacar(self, transacao : Saque) -> None:
        """Realiza um saque na conta, respeitando as regras de negócio 
        (Limites de saques diários e valor máximo de saque)"""
        assert((isinstance(transacao, Saque)) and (transacao.valor > 0))

        if transacao.valor > self.MAX_SAQUE:
            print(f"Valor de saque máximo excedeu o limite de R${self.MAX_SAQUE:.2f}!")
            return

        if self.__saldo <= 0:
            print("Saldo insuficiente")
            return

        if self.__saques >= self.LIMITE_SAQUES:
            print(f"Limite de {self.LIMITE_SAQUES} saques diários atingido")
            return

        self.__saldo -= transacao.valor
        self.__extrato.nova_transacao(transacao=transacao)
        self.__saques += 1

        print(f"Saque de R${transacao.valor:.2f} efetuado.")

    def __str__(self) -> str:
        return f"""
        Conta: {self.__numero}
        Saldo: R${self.__saldo}
        
        Limite de saque: R${self.MAX_SAQUE}
        Saques disponíveis: {self.LIMITE_SAQUES - self.__saques}"""

    @staticmethod
    def nova_conta() -> 'Conta':
        """Função estática para auxiliar na criação de uma nova conta"""

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
    """
    Função que imprime o menu disponível e retorna a escolha do usuário
    """
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
            valor = float(input("Insira o valor: R$"))
            conta_selecionada.depositar(Deposito(valor))
            input()

        if acao == 'S':
            print('Saque:')
            valor = float(input("Insira o valor: R$"))
            conta_selecionada.sacar(Saque(valor))
            input()

        if acao == 'E':
            print(conta_selecionada.extrato)
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

            conta_numero : Conta = None

            for conta in contas:
                if conta.numero == numero:
                    if conta.senha == senha:
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
