# Sistema Bancário Simples com Python

## **Simulador de Caixa Eletrônico**

* O código simula as principais funções de um caixa eletrônico, como depósito, saque e consulta de saldo.
* O sistema utiliza variáveis para armazenar informações como saldo, limite de saque, extrato e número de saques realizados.
* O código demonstra o uso de estruturas de controle como `if`, `elif` e `while` para controlar o fluxo do programa e responder às entradas do usuário.
* O código utiliza funções básicas de formatação de strings para apresentar informações de forma organizada e legível.

**Conceitos aprendidos:**

* **Variáveis:** Armazenamento de dados durante a execução do programa.
* **Estruturas de controle:** `if`, `elif` e `while` para controlar o fluxo do programa.
* **Funções:** Funções básicas de formatação de strings.
* **Lógica de programação:** Implementação de regras e lógica para simular o funcionamento do caixa eletrônico.

**Habilidades desenvolvidas:**

* **Leitura e análise de código Python:** Compreender o código e identificar as diferentes partes que o compõem.
* **Modificação e adaptação do código:** Alterar o código para adicionar novas funcionalidades ou modificar o comportamento do programa.
* **Depuração de código:** Identificar e corrigir erros no código para garantir o funcionamento correto do programa.

**Aplicações:**

* O código pode ser usado como base para projetos mais complexos, como um sistema bancário completo.
* Os conceitos aprendidos podem ser aplicados em diversos outros contextos de programação.

**Observações:**

* O código é um exemplo simples e pode ser adaptado para atender às necessidades específicas de cada projeto.
* É importante seguir boas práticas de programação para garantir a qualidade e a legibilidade do código.

<details>
<summary>Código-fonte</summary>

**LAB-01** - [/lab-01.py](./lab-01.py)

```python
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
```
</details>
