menu = """
++=======================++
||      Virtus Bank      ||
||                       ||
||     [1] Depositar     ||
||     [2] Sacar         ||
||     [3] Extrato       ||
||     [0] Sair          ||
||                       ||
++=======================++

Digite a sua opção: """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Erro! O valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Erro! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Erro! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Erro! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Erro! O valor informado é inválido.")

    elif opcao == "3":
            print(
                """
===========================
        Virtus Bank      
          EXTRATO        
                         
{}                       
                         
    Saldo: R$ {:.2f}     
                         
===========================
""".format(
                    extrato if extrato else "Sem movimentações.",
                    saldo,
                )
            )

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
