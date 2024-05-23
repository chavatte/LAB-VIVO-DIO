# Projeto TDD: Construindo uma API com FastAPI e Testes com Pytest

<img align="center" src="./assets/screenshot.png" />

<details>
<summary>O que é TDD (Test Driven Development)?</summary>

TDD, ou Desenvolvimento Orientado a Testes, é uma abordagem de desenvolvimento de software que prioriza a criação de testes antes da implementação do código. Essa metodologia promove ciclos de desenvolvimento mais curtos e garante uma maior qualidade do software

### Ciclo do TDD
![C4](./assets/img-tdd.png)

### Vantagens do TDD
* **Software de alta qualidade:** A aplicação é construída com foco na qualidade desde o início.
* **Identificação de falhas:** Os testes ajudam a encontrar e corrigir erros precocemente.
* **Testes abrangentes:** Criação de testes unitários, de integração e outros tipos de testes.
* **Código conciso e eficiente:** Evita a criação de código desnecessário ou complexo.
* **Requisitos bem definidos:** Garante que o código atenda aos requisitos estabelecidos.

</details>
<details>
<summary>Store API: Um projeto de aprendizado prático</summary>

### Resumo do projeto
Este projeto tem como objetivo demonstrar a aplicação do TDD na prática, através do desenvolvimento de uma API RESTful utilizando o framework FastAPI. A API interage com um banco de dados MongoDB e utiliza o Pydantic para validação de dados. Os testes são implementados com o Pytest.

### Objetivo
O principal objetivo deste projeto é proporcionar um ambiente de aprendizado prático sobre TDD, utilizando tecnologias modernas como FastAPI e Pytest.

### O que a API faz
* **Fins educativos:** A API foi criada para fins de aprendizado e demonstração.
Aprendizado prático: Permite que você aprenda TDD de forma prática, construindo uma API completa.

### O que a API NÃO faz
* **Comunicação externa:** A API não se integra com outras aplicações externas.

### Solução Proposta
Desenvolvimento de uma API simples, seguindo os princípios do TDD, com testes abrangentes utilizando o Pytest. Os testes incluem validação de schemas, casos de uso e testes de integração dos controladores.

### Arquitetura
|![C4](./assets/store.drawio.png)|
|:--:|
| Diagrama de C4 da Store API |

### Banco de dados - MongoDB
|![C4](./assets/product.drawio.png)|
|:--:|
| Database - Store API |

</details>
<details>
<summary>Diagramas de sequência para o módulo de Produtos</summary>

### Diagrama de criação de produto

```mermaid
sequenceDiagram
    title Create Product
    Client->>+API: Request product creation
    Note right of Client: POST /products

    API->>API: Validate body

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request product creation
    alt Error on insertion
        API->Client: Error Response
        note right of Client: Status Code: 500 - Internal Server Error
        end
    Database->>-API: Successfully created

    API->>-Client: Successful Response
    Note right of Client: Status Code: 201 - Created

```
### Diagrama de listagem de produtos

```mermaid
sequenceDiagram
    title List Products
    Client->>+API: Request products list
    Note right of Client: GET /products

    API->>+Database: Request products list

    Database->>-API: Successfully queried

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```

### Diagrama de detalhamento de um produto

```mermaid
sequenceDiagram
    title Get Product
    Client->>+API: Request product
    Note right of Client: GET /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>+Database: Request product
    alt Error on query
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    else Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully queried

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```
### Diagrama de atualização de produto

```mermaid
sequenceDiagram
    title PUT Product
    Client->>+API: Request product update
    Note right of Client: PUT /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>API: Validate body

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request product
    alt Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully updated

    API->>-Client: Successful Response
    Note right of Client: Status Code: 200 - Ok
```

### Diagrama de exclusão de produto

```mermaid
sequenceDiagram
    title Delete Product
    Client->>+API: Request product delete
    Note right of Client: DELETE /products/{id}<br/> Path Params:<br/>    - id: <id>

    API->>+Database: Request product
    alt Product not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
        end

    Database->>-API: Successfully deleted

    API->>-Client: Successful Response
    Note right of Client: Status Code: 204 - No content
```
</details>
