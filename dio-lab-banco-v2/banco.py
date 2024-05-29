# Melhorando o codigo do banco utlizando funções

menu = """
    ============ MENU ============

        [1] - Saque
        [2] - Deposito
        [3] - Extrato
        [4] - Cadastrar Usuario
        [5] - Cadastrar Conta Bancaria
        [6] - Listar Contas
        [7] - Sair

    ==============================

"""

def sacar(*, saldo, saque, numero_saques, extrato, limite, limite_saques):
    print("\n=========== Saque ===========")
    if numero_saques < limite_saques:
            if saque > 0 and saque <= limite:
                if saque <= saldo:
                    saldo -= saque
                    print(f"Saque no valor de R$ {saque:.2f} realizado com sucesso!")
                    numero_saques += 1
                    extrato += f"Saque: R${saque:.2f} \n"
                else:
                    print("Saldo insuficiente!")
            else:
                print("Valor de saque invalido!")
    else:
        print("Você ja atingiu o limite de três saques diarios")    
    return saldo, extrato


def deposito(saldo, valor, extrato, /):
    print("\n========= Deposito =========")
    if valor > 0 :
        saldo += valor
        print(f"Deposito no valor de R${valor:.2f} realizado com sucesso!")
        extrato += f"Deposito: R${valor:.2f} \n"
    else:
        print("Valor de deposito invalido!")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n========= Extrato =========")
    print("Ainda não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual = R$ {saldo:.2f}")


def cadastrar_usuario(usuarios):
    print("\n===== Criando Usuario =====")
    cpf = input("Entre com o cpf (apenas os numeros):")

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Ja existe usuario cadastrado com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuario cadastrado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def cadastrar_conta(agencia, contas_corrente, usuarios):
    print("\n========= Criando Conta Corrente ==========")
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta corrente criada com sucesso!")
        numero_conta = len(contas_corrente) + 1
        contas_corrente.append({"numero_conta": numero_conta, "agencia": agencia, "usuario": usuario})
    else:
        print("Usuário não encontrado!")


def listar_usuarios(usuarios):
    print("\n======== Lista de Usuarios =============")
    for usuario in usuarios:
        print(usuario)


def listar_contas(contas_corrente):
    print("\n============ Lista de Contas ===========")
    for conta in contas_corrente:
        print(
            conta
        )


def main():
    saldo = 1000
    limite = 500
    numero_saques = 0
    extrato = ""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas_corrente = []
    numero_conta = 0



    while True:
        opcao = input(menu + "Escolha uma opção: ")
        if opcao == "1":
            #("=========== Saque ===========")
            saque = float(input("Qual valor gostaria de sacar? "))
            saldo, extrato = sacar(
                saldo=saldo, 
                saque=saque,
                numero_saques=numero_saques, 
                extrato=extrato,
                limite=limite,
                limite_saques=LIMITE_SAQUES)

        elif opcao == "2":
            #("========= Deposito =========")
            valor = float(input("Qual valor gostaria de depositar? "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "3":
            #("========= Extrato =========")
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            #(======= Cadastrar Usuario ========)
            cadastrar_usuario(usuarios)

        elif opcao == "5":
            #(====== Cadastrar Conta Corrente =========)
            cadastrar_conta(AGENCIA, contas_corrente, usuarios)

        elif opcao == "6":
            #(====== Listar Contas =======)
            listar_contas(contas_corrente)

        elif opcao == "7":
            #(====== Sair ======)
            break
            
        else:
            print("Opção invalida!")

main()