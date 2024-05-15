saldo = 1000
limite = 500
numero_saques = 0
extrato = ""
LIMITE_SAQUES = 3

menu = """
    ============ MENU ============

        [1] - Saque
        [2] - Deposito
        [3] - Extrato
        [4] - Sair

    ==============================

"""

while True:
    opcao = int(input(menu + "Escolha uma opção: "))
    if opcao == 1:
        if numero_saques < LIMITE_SAQUES:
            print("=========== Saque ===========")
            saque = float(input("Qual valor gostaria de sacar? "))
            if saque > 0 and saque <= limite:
                if saque <= saldo:
                    saldo -= saque
                    print(f"Saque no valor de R$ {saque:.2f} realizado com sucesso!")
                    numero_saques += 1
                    extrato += f"Saque: R${saque:.2f} \n"
                else:
                    print("Saldo insuficiente")
            else:
                print("Valor de saque invalido!")
        else:
            print("Você ja atingiu o limite de três saques diarios")

    elif opcao == 2:
        print("========= Deposito =========")
        deposito = float(input("Qual valor gostaria de depositar? "))
        if deposito > 0 :
            saldo += deposito
            extrato += f"Deposito: R${deposito:.2f} \n"
        else:
            print("Valor de deposito invalido")

    elif opcao == 3:
        print("========= Extrato =========")
        print(extrato)
        print(f"Saldo atual = R$ {saldo:.2f}")

    elif opcao == 4:
        break

    else:
        print("Opção invalida!")