import textwrap
import random

def menu():
    menu = """
++=======================++
||      Virtus Bank      ||
||                       ||
||     [1] Depositar     ||
||     [2] Sacar         ||
||     [3] Extrato       ||
||     [4] Novo Usuário  ||
||     [5] Nova Conta    ||
||     [6] Listar Contas ||
||     [0] Sair          ||
||                       ||
++=======================++

Digite a sua opção: """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Erro! O valor informado é inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Erro! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Erro! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Erro! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")

    else:
        print("Erro! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
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
    input("Pressione Enter para continuar...")

def criar_usuario(usuarios):
  while True:
    cpf = input("Informe o CPF (somente números): ")
    if not cpf.isdigit() or len(cpf) != 11:
      print("CPF inválido. Digite novamente (somente números): ")
      continue
    break
  usuario = filtrar_usuario(cpf, usuarios)

  if usuario:
    print("Já existe usuário com esse CPF!")
    return

  nome = input("Nome Completo: ")
  while True:
    data_nascimento = input("Data de Nascimento (DDMMAAAA): ")
    if not data_nascimento.isdigit() or len(data_nascimento) != 8:
      print("Data de Nascimento inválida. Digite novamente (DDMMAAAA): ")
      continue
    break
#   data_nascimento = input("Data de Nascimento (dd-mm-aaaa): ")
  logradouro = input("Logradouro: ")
  numero = input("Número: ")
  complemento = input("Complemento (opcional): ")
  bairro = input("Bairro: ")
  cidade = input("Cidade: ")
  estado = input("Estado: ")
  cep = input("CEP (somente números): ")
  while not cep.isdigit() or len(cep) != 8:
    cep = input("CEP inválido. Digite novamente (somente números): ")

  data_nascimento_formatada = f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"
  cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}/{cpf[9:]}"
  cep_formatado = f"{cep[:5]}-{cep[5:]}"
  endereco = f"{logradouro}, {numero} {'- ' + complemento if complemento else ''}"
  localidade = f"{bairro} - {cidade}/{estado}"
  usuario = {"nome": nome, "data_nascimento_formatada": data_nascimento_formatada, "cpf": cpf, "cpf_formatado": cpf_formatado, "endereco": endereco, "localidade": localidade, "cep_formatado": cep_formatado}

  usuarios.append(usuario)

  print("*" * 40)
  print(f"""
    Usuário criado com sucesso!
        4
        
    Dados do Inseridos:

  CPF: {usuario['cpf_formatado']}
  Nome: {usuario['nome']}
  Data de Nascimento: {usuario['data_nascimento_formatada']}
  Endereço: {usuario['endereco']}
  Localidade: {usuario['localidade']}
  CEP: {usuario['cep_formatado']}
  """)
  print("*" * 40)
  input("Pressione Enter para continuar...")
  
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    numero_conta = random.randint(100000, 999999)
    numero_conta_formatado = f"{numero_conta}-0"
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}/{cpf[9:]}"

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta_formatado, "usuario": usuario, "cpf_formatado": cpf_formatado}

    print("Usuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            CPF:\t\t{conta['cpf_formatado']}
            Titular:\t{conta['usuario']['nome']}
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
        """
        print("*" * 40)
        print(textwrap.dedent(linha))
        input("Pressione Enter para continuar...")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
