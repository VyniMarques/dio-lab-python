from abc import ABC, abstractmethod

class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo

        if valor > saldo:
            print("\nOperação falhou, saldo insuficiente! ")
        elif valor > 0:
            self._saldo -= valor
            print("\nOperação realizada com sucesso!")
            return True
        else:
            print("\nOperação falhou, valor invalido!")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizdo com sucesso!")
        else:
            print("Valor de deposito invalido")
            return False
        return True

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
        )

        if valor > self.limite:
            print("\nOperação falhou! O valor do saque excede o limite. ")

        elif numero_saques >= self.limite_saques:
            print("\nOperação falhou! Número máximo de saques excedido. ")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo ": transacao.__class__.__name__,
            "valor": transacao.valor
        })

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def sacar(clientes):
    print("\n=========== Saque ===========")

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))

    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    print("\n========= Deposito =========")

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do deposito: "))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    return cliente.contas[0]

def exibir_extrato(clientes):
    print("\n========= Extrato =========")

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    
def cadastrar_cliente(clientes):
    print("\n========= Cadastrando Cliente =========")

    cpf = input("Informe o CPF (apenas os numeros):")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJa existe cliente cadastrado com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in 
    clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def cadastrar_conta(numero_conta, clientes, contas):
    print("\n========= Criando Conta Corrente ==========")

    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")

def listar_contas(contas_corrente):
    print("\n============ Lista de Contas ===========")
    for conta in contas_corrente:
        print(
            str(conta)
        )

def menu():
    menu = """
    ============ MENU ============

        [1] - Saque
        [2] - Deposito
        [3] - Extrato
        [4] - Cadastrar Cliente
        [5] - Cadastrar Conta
        [6] - Listar Contas
        [7] - Sair

    ==============================
    """
    return input(menu)

def main():

    clientes = []
    contas = []
    

    while True:
        opcao = menu()
        if opcao == "1":
            #("=========== Saque ===========")
            sacar(clientes)

        elif opcao == "2":
            #("========= Deposito =========")
            depositar(clientes)

        elif opcao == "3":
            #("========= Extrato =========")
            exibir_extrato(clientes)

        elif opcao == "4":
            #(======= Cadastrar Usuario ========)
            cadastrar_cliente(clientes)

        elif opcao == "5":
            #(====== Cadastrar Conta Corrente =========)
            numero_conta = len(contas) + 1
            cadastrar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            #(====== Listar Contas =======)
            listar_contas(contas)

        elif opcao == "7":
            #(====== Sair ======)
            break
            
        else:
            print("Opção invalida!")

main()