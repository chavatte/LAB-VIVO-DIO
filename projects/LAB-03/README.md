# Modelando o Sistema Bancário em POO com Python

O sistema implementado no Lab-03 apresenta uma base sólida para o desenvolvimento de um sistema bancário completo.
As funcionalidades básicas de gerenciamento de contas (depósito, saque e consulta de extrato) estão funcionando corretamente.
O código foi estruturado e organizado, o que facilita a compreensão e a manutenção do sistema.
As melhorias em relação ao Lab-02 demonstram aprimoramento e implementação de novas funcionalidades.

## Modificações, implementações e melhorias no lab-03 em relação ao Lab-02:

**Funcionalidades:**

* **Criação de clientes:**
  * Implementado o cadastro de clientes com as informações: nome, data de nascimento, endereço completo (logradouro, número, complemento, bairro, cidade, estado) e CEP.
  * A validação do CPF foi aprimorada para garantir que ele esteja no formato correto (somente números, com 11 dígitos).
  * A data de nascimento também é validada para garantir que esteja no formato DDMMAAAA.
  * O sistema armazena os clientes em uma lista (`clientes`).
* **Criação de contas:**
  * Implementada a funcionalidade de criação de contas correntes para os clientes cadastrados.
  * O número da conta é gerado aleatoriamente e formatado com dígito verificador.
  * A conta é associada ao cliente e armazenada em uma lista de contas do cliente (`contas`).
  * As contas são armazenadas em um dicionário (`contas_por_cpf`), onde a chave é o CPF do cliente e o valor é a lista de contas desse cliente.
* **Gerenciamento de contas:**
  * O sistema permite realizar operações de depósito, saque e consulta de extrato em contas correntes.
  * A validação do valor do depósito e do saque foi aprimorada para garantir que seja um valor positivo.
  * O histórico das transações (depósitos e saques) é armazenado na conta (`historico`).
  * O extrato da conta apresenta as transações agrupadas por tipo (depósito e saque), com data, hora e valor formatados.
* **Listagem de contas:**
  * Implementada a funcionalidade de listar as contas de um cliente, informando agência, número da conta, saldo e nome do cliente.
  * As informações do cliente (nome, data de nascimento, endereço e CEP) também são exibidas na listagem.

**Melhorias:**

* **Organização do código:**
  * O código foi dividido em módulos (`Cliente`, `Conta`, `Historico`, `Transacao`, `Saque`, `Deposito`, etc.) para melhorar a organização e legibilidade.
  * O código segue as convenções de nomenclatura PEP8.
* **Validação de dados:**
  * A validação de dados foi aprimorada para garantir que os valores informados pelo usuário sejam válidos e consistentes.
  * Mensagens de erro mais informativas foram implementadas para auxiliar o usuário na correção de erros.
* **Interface do usuário:**
  * A interface do usuário foi aprimorada com a utilização de menus e prompts interativos para facilitar a navegação e utilização do sistema.
  * As informações são exibidas de forma formatada e clara para o usuário.
* **Segurança:**
  * O sistema armazena as informações dos clientes e contas de forma segura, utilizando listas e dicionários em memória.

<details>
<summary>Código-fonte</summary>

**LAB-03** - [/lab-03.py](./lab-03.py)

```python
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
import random

contas_por_cpf = {}
contas = []
clientes = []

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento_formatada, cpf, cpf_formatado, endereco, localidade, cep_formatado):
        super().__init__(endereco)
        self.localidade= localidade
        self.cep_formatado= cep_formatado
        self.nome = nome
        self.data_nascimento_formatada = data_nascimento_formatada
        self.cpf = cpf
        self.cpf_formatado= cpf_formatado

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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Erro! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            transacao_saque = Saque(valor)
            if not transacao_saque in self.historico.transacoes:
                self.historico.adicionar_transacao(transacao_saque)
            return True

        else:
            print("Erro! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
        else:
            print("Erro! O valor informado é inválido.")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Erro! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Erro! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )

class Transacao(ABC):
    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass

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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Erro! Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF (somente números) do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    contas = cliente.contas

    if not contas:
        print("Cliente não possui conta!")
        return

    print("\nSelecione a conta para depósito:")
    for i, conta in enumerate(contas):
        print(f"  {i+1} - Agência: {conta.agencia} - Número: {conta.numero}")

    numero_conta_escolhida = int(input("Digite o número da conta: "))

    if numero_conta_escolhida <= 0 or numero_conta_escolhida > len(contas):
        print("Conta inválida!")
        return

    conta_escolhida = contas[numero_conta_escolhida - 1]

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta_escolhida, transacao)
    valor_formatado = f"{valor:.2f}"
    conta_formatada = f"Agência: {conta_escolhida.agencia} - Número: {conta_escolhida.numero}"

    print(f"""
Depósito realizado com sucesso!

Conta: {conta_formatada}
Valor: R$ {valor_formatado}
""")
    input("Pressione Enter para continuar...")

def sacar(clientes):
    cpf = input("Informe o CPF (somente números) do cliente: ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    contas = cliente.contas

    if not contas:
        print("Cliente não possui conta!")
        return

    print("\nSelecione a conta para saque:")
    for i, conta in enumerate(contas):
        print(f"  {i+1} - Agência: {conta.agencia} - Número: {conta.numero}")

    numero_conta_escolhida = int(input("Digite o número da conta: "))

    if numero_conta_escolhida <= 0 or numero_conta_escolhida > len(contas):
        print("Conta inválida!")
        return

    conta_escolhida = contas[numero_conta_escolhida - 1]

    valor = float(input("Informe o valor do saque: "))

    if valor <= 0:
        print("Valor do saque inválido!")
        return

    if not conta_escolhida.sacar(valor):
        print("Saque não realizado!")
        return

    valor_formatado = f"{valor:.2f}"
    conta_formatada = f"Agência: {conta_escolhida.agencia} - Número: {conta_escolhida.numero}"

    print(f"""
Saque realizado com sucesso!

Conta: {conta_formatada}
Valor: R$ {valor_formatado}
""")
    input("Pressione Enter para continuar...")

def exibir_extrato(clientes):
    while True:
        cpf = input("Informe o CPF (somente números) do cliente: ")

        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Digite novamente (somente números): ")
            continue

        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print(f"Cliente com CPF {cpf} não encontrado.")
            break

        contas_do_cliente = cliente.contas
        if not contas_do_cliente:
            print(f"Cliente com CPF {cpf} não possui contas.")
            break

        if len(contas_do_cliente) == 1:
            conta_escolhida = contas_do_cliente[0]
            exibir_extrato_conta(conta_escolhida)
            break

        print("\n**Contas do CPF:**", cpf)
        for i, conta in enumerate(contas_do_cliente):
            print(f"{i+1} - Agência: {conta.agencia} - Número: {conta.numero}")

        numero_conta_escolhida = int(input("Digite o número da conta: "))

        if numero_conta_escolhida <= 0 or numero_conta_escolhida > len(contas_do_cliente):
            print("Conta inválida. Digite novamente o número da conta: ")
            continue

        conta_escolhida = contas_do_cliente[numero_conta_escolhida - 1]
        exibir_extrato_conta(conta_escolhida)
        return

def exibir_extrato_conta(conta):
    print("\nExtrato da Conta:", conta.numero)
    print("-" * 20)

    transacoes = conta.historico.transacoes

    transacoes_agrupadas = {}
    for transacao in transacoes:
        tipo_transacao = transacao["tipo"]
        if tipo_transacao not in transacoes_agrupadas:
            transacoes_agrupadas[tipo_transacao] = []
        transacoes_agrupadas[tipo_transacao].append(transacao)

    for tipo_transacao, transacoes_tipo in transacoes_agrupadas.items():
        print(f"\n{tipo_transacao.upper()}:")
        for transacao in transacoes_tipo:
            valor = transacao["valor"]
            data_hora = transacao["data"]
            valor_formatado = f"R${valor:.2f}"
            data_hora_formatada = f"{data_hora[:10]} {data_hora[11:]}"
            print(f"{data_hora_formatada} --> {valor_formatado}")
    print(f"\nSaldo Atual:")
    print(f"R${conta.saldo:.2f}")
    print("-" * 20)

    input("Pressione Enter para continuar...")

def criar_cliente(clientes):
  while True:
    cpf = input("Informe o CPF (somente números): ")
    if not cpf.isdigit() or len(cpf) != 11:
      print("CPF inválido. Digite novamente (somente números): ")
      continue
    break

  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("Já existe cliente com esse CPF!")
    return

  nome = input("Nome Completo: ")

  while True:
    data_nascimento = input("Data de Nascimento (DDMMAAAA): ")
    if not data_nascimento.isdigit() or len(data_nascimento) != 8:
      print("Data de Nascimento inválida. Digite novamente (DDMMAAAA): ")
      continue
    break

  logradouro = input("Logradouro: ")
  numero = input("Número: ")
  complemento = input("Complemento (opcional): ")
  bairro = input("Bairro: ")
  cidade = input("Cidade: ")
  estado = input("Estado: ")

  while True:
    cep = input("CEP (somente números): ")
    if not cep.isdigit() or len(cep) != 8:
      print("CEP inválido. Digite novamente (somente números): ")
      continue
    break

  data_nascimento_formatada = f"{data_nascimento[:2]}/{data_nascimento[2:4]}/{data_nascimento[4:]}"
  cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}/{cpf[9:]}"
  cep_formatado = f"{cep[:5]}-{cep[5:]}"

  endereco = f"{logradouro}, {numero} {'- ' + complemento if complemento else ''}"
  localidade = f"{bairro} - {cidade}/{estado}"

  cliente = PessoaFisica(
      nome=nome,
      data_nascimento_formatada=data_nascimento_formatada,
      cpf=cpf,
      cpf_formatado=cpf_formatado,
      endereco=endereco,
      localidade=localidade,
      cep_formatado=cep_formatado,
  )

  clientes.append(cliente)

  print("*" * 40)
  print(f"""
    Cliente criado com sucesso!

    Dados do Inseridos:

    CPF: {cliente.cpf_formatado}
    Nome: {cliente.nome}
    Data de Nascimento: {cliente.data_nascimento_formatada}
    Endereço: {cliente.endereco}
    Localidade: {cliente.localidade}
    CEP: {cliente.cep_formatado}
    """)
  print("*" * 40)
  input("Pressione Enter para continuar...")

def criar_conta(agencia, clientes):
  while True:
    cpf = input("Informe o CPF do cliente (sem formatação): ")
    if not cpf.isdigit() or len(cpf) != 11:
      print("CPF inválido. Digite novamente (somente números): ")
      continue
    break

  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado, fluxo de criação de conta encerrado!")
    return

  numero_conta = random.randint(100000, 999999)
  numero_conta_formatado = f"{numero_conta}-0"
  cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}/{cpf[9:]}"

  conta = ContaCorrente(
      numero=numero_conta_formatado,
      cliente=cliente,
  )

  cliente.contas.append(conta)
  contas_por_cpf.setdefault(cliente.cpf, []).append(conta)

  print("*" * 40)
  print(f"""
    Conta criada com sucesso!

    Dados da Conta:

    CPF: {cpf_formatado}
    Cliente: {cliente.nome}
    Agência: {agencia}
    Número da Conta: {numero_conta_formatado}
  
  
    """)
  print("*" * 40)
  input("Pressione Enter para continuar...")
  
def listar_contas(contas_por_cpf):
    while True:
        cpf = input("Informe o CPF do cliente (somente números): ")
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}/{cpf[9:]}"
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Digite novamente (somente números): ")
            continue

        if cpf not in contas_por_cpf:
            print(f"Cliente com CPF {cpf_formatado} não encontrado.")
            return

        contas_do_cliente = contas_por_cpf[cpf]

        if not contas_do_cliente:
            print(f"Cliente com CPF {cpf_formatado} não possui contas.")
            return
        cliente = contas_do_cliente[0].cliente
        print("*" * 40)
        print(f"Contas do CPF: {cpf_formatado}")
        print("*" * 40)
        print(f"""
    Dados Cadastrados:
Nome: {cliente.nome}
Data de Nascimento: {cliente.data_nascimento_formatada}
Endereço: {cliente.endereco}
Localidade: {cliente.localidade}
CEP: {cliente.cep_formatado}
      
    Contas:""")
        for conta in contas_do_cliente:
            print(f"""
Agência: {conta.agencia}
Número da Conta: {conta.numero}
Saldo: R${conta.saldo:.2f}
            """)
            print("*" * 40)
        input("Pressione Enter para continuar...")
        break

def main():
    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            agencia = "0001"
            criar_conta(agencia, clientes)

        elif opcao == "6":
            listar_contas(contas_por_cpf)

        elif opcao == "0":
            print(f"""
++=======================++
||      Virtus Bank      ||
||                       ||
||       Saindo do       ||
||        Sistema        ||
++=======================++
""")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
```

</details>
