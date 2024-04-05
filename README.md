# Desafio Pecege

O Desafio Pecege é um projeto que surge como uma proposta técnica do Instituto Pecege, com o objetivo de explorar habilidades em desenvolvimento Python. Este desafio é composto por quatro fases distintas, cada uma exigindo o uso de diversas tecnologias e técnicas para sua resolução. Neste projeto, além da resolução das fases, foram implementadas algumas tecnologias com o objetivo de melhorar a performance do código e a experiência do usuário da aplicação.


## Tecnologias Utilizadas

Ao longo das fases do Desafio Pecege, foram empregadas diversas tecnologias, incluindo:

- **Biblioteca Pokebase:** Utilizada para conexão e interação com a PokeAPI, permitindo a obtenção de informações sobre os Pokémon.
- **Banco de Dados SQLite:** Empregado para armazenamento local dos dados dos Pokémon, possibilitando consultas e operações de manipulação, além de melhorar a performance do código, possibilitando com uma única requisição para api armazenar os dados e sempre que for necessário criar o gráfico com a quantidade de pokemons, importar esses dados do banco ganhando assim mais performance no momento da requisição do usuário.
- **Biblioteca Numpy:** Utilizada para manipulação eficiente de arrays multidimensionais e cálculos numéricos, mais especificamente nesse projeto na criação de um array que varia de 0 a 1, fazendo com que a quantidade de pontos seja igual ao número de tipos do pokemon gerando uma posição ao longo do mapa de cores viridis que é disponibilizado pela biblioteca matplotlib. Sendo assim, cada barra de tipos de pokemon vai ter uma cor diferente de acordo com sua quantidade.
- **Biblioteca Matplotlib:** Utilizada para geração de gráficos, permitindo a visualização dos tipos dominantes dos Pokémon em forma de barras.
- **Biblioteca Pandas:** Utilizada para manipulação e análise de dados, permitindo a criação de DataFrames com os dados dos Pokémon especificamente neste projeto, foi utilizada para obter o nome, peso, altura e tipo dos pokemons, retorná-los no terminal e criar um arquivo Excel para visualização.
- **Framework FastAPI:** Utilizado para transformar um código Flask em uma API web mais eficiente, com suporte a tipagem de dados e outras funcionalidades avançadas.

Essas tecnologias foram selecionadas e combinadas de forma a abordar os desafios propostos de maneira eficiente e escalável.


## Sumário:

I. **Fases**

II. **Instalação**

III. **Utilização**

IV. **Licença**

V. **Contato/Contribuição**



## I. **FASES**
   
### Fase 1: Verificação de Query SQL


Considere a query a seguir e responda. É um SQL funcional ou possui algum erro? 
Caso possua algum erro, comente e corrija. 


````
select count(distinct origin_registration_id), new_status, old_status,
from registrations_fact
where new_status == (1, 2, 3, 4, 5, 6)
order by new_status
group by new_status;
````

Código corrigido

````
SELECT COUNT(DISTINCT origin_registration_id) AS count_origin_registration, new_status, old_status 
    FROM registrations_fact
    WHERE new_status IN (1, 2, 3, 4, 5, 6) 
    GROUP BY new_status
    ORDER BY new_status
````

A query fornecida possui alguns erros que foram corrigidos. Abaixo estão os erros identificados e suas correções:

1. **Uso incorreto de `==` em vez de `IN`:**
   O operador `==` é usado para verificar a igualdade entre duas expressões. No entanto, para verificar se uma coluna está em um conjunto de valores, devemos usar a cláusula `IN`. Portanto, o trecho `new_status == (1, 2, 3, 4, 5, 6)` foi corrigido para `new_status IN (1, 2, 3, 4, 5, 6)`.

2. **Vírgula extra após a lista de colunas no `SELECT`:**
   Na declaração `SELECT`, não deve haver uma vírgula após a última coluna da lista de seleção. Portanto, a vírgula após `distinct origin_registration_id` foi removida.

3. **Ordem incorreta das cláusulas `GROUP BY` e `ORDER BY`:**
   A cláusula `GROUP BY` deve ser especificada antes da cláusula `ORDER BY`. Portanto, a ordem das cláusulas `GROUP BY` e `ORDER BY` foram trocadas.

4. **Utilização da expressão `AS count_origin_registration`:**
   Não foi um erro do código, mas foi usada para atribuir um alias à função de agregação `COUNT(DISTINCT origin_registration_id)`. Quando uma função de agregação é usada em uma consulta SQL, o resultado normalmente não tem um nome associado diretamente, o que pode dificultar a identificação do que está sendo representado, especialmente em consultas mais complexas.

### Fase 2: Conexão à PokeAPI e Gráfico de Barras


Conecte-se à PokeAPI através da biblioteca pokebase, e retorne em um gráfico de 
barras, os dados de tipo dominante dos 100 primeiros pokémons disponíveis, de 
forma a agrupá-los e mostrá-los em ordem decrescente. 

<img src="images_readme/Captura de tela 2024-04-05 190105.png" alt="Gráfico">



````
import pokebase as pb
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

def criar_tabela_se_nao_existir():
    
    conn = sqlite3.connect('pokemons.db')
    c = conn.cursor()

    
    c.execute('''CREATE TABLE IF NOT EXISTS pokemon (
                 id INTEGER PRIMARY KEY,
                 nome TEXT,
                 tipo1 TEXT,
                 tipo2 TEXT)''')

    
    conn.commit()

    
    conn.close()

def buscar_e_armazenar_pokemon(num_pokemon):
    
    conn = sqlite3.connect('pokemons.db')
    c = conn.cursor()

    
    c.execute('SELECT COUNT(*) FROM pokemon')
    quantidade_pokemon = c.fetchone()[0]

    
    if quantidade_pokemon < num_pokemon:
        for i in range(quantidade_pokemon + 1, num_pokemon + 1):
            
            c.execute('SELECT COUNT(*) FROM pokemon WHERE id = ?', (i,))
            if c.fetchone()[0] == 0:
                pokemon = pb.pokemon(i)
                nome = pokemon.name
                tipo1 = pokemon.types[0].type.name
                tipo2 = pokemon.types[1].type.name if len(pokemon.types) > 1 else None
                c.execute('INSERT INTO pokemon (id, nome, tipo1, tipo2) VALUES (?, ?, ?, ?)', (i, nome, tipo1, tipo2))

        
        conn.commit()

    
    c.execute('SELECT tipo1 FROM pokemon LIMIT ?', (num_pokemon,))
    tipos = [row[0] for row in c.fetchall()]

    
    contagem_tipo = {}
    for t in tipos:
        contagem_tipo[t] = contagem_tipo.get(t, 0) + 1

    
    contagem_tipo = dict(sorted(contagem_tipo.items(), key=lambda item: item[1], reverse=True))

    
    tipos = list(contagem_tipo.keys())
    frequencias = list(contagem_tipo.values())

    
    cores = plt.cm.viridis(np.linspace(0, 1, len(tipos)))

    
    plt.figure(figsize=(10, 6))

    
    barras = plt.bar(tipos, frequencias, color=cores)

    
    plt.xlabel('Tipo Dominante')
    
    plt.ylabel('Número de Pokémon')
    
    plt.title(f'Tipos Dominantes dos {num_pokemon} primeiros Pokémon')

    
    legendas = [f'{tipo} ({freq})' for tipo, freq in zip(tipos, frequencias)]
    plt.legend(barras, legendas)

    
    plt.xticks(rotation=45)

    
    plt.tight_layout()

    
    plt.show()

    
    conn.close()

def main():
    while True:
        try:
            num_pokemon_requisitados = int(input("Quantos Pokémon você deseja requisitar? "))
            if num_pokemon_requisitados <= 0:
                print("Número inválido de Pokémon. Por favor, insira um número maior que zero.")
                continue
            criar_tabela_se_nao_existir()  
            buscar_e_armazenar_pokemon(num_pokemon_requisitados)
            escolha = input("Deseja fazer outra consulta? (S/N): ").strip().upper()
            if escolha != 'S':
                print("Encerrando o programa...")
                break
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

if __name__ == "__main__":
    main()

````

### Fase 3: Criação de DataFrame com os Dados dos Pokémon


Ainda usando a PokeAPI, crie e retorne um dataframe com os dados dos 50 
primeiros pokémons, incluindo, nome, peso, altura e tipo. 


````
import pandas as pd
import requests

link = "https://pokeapi.co/api/v2/pokemon/"
pokemons = []

for i in range(1, 51):   
    response = requests.get(link + str(i))
    if response.status_code == 200:
        data = response.json()
        pokemon_data = {
            'Nome': data['name'],
            'Peso': data['weight'],
            'Altura': data['height'],
            'Tipo': ', '.join([t['type']['name'] for t in data['types']])
        }
        pokemons.append(pokemon_data)

df = pd.DataFrame(pokemons)
print(df)
df.to_excel('pokemon.xlsx', index=False)
````

### Fase 4: Transformação para FastAPI


Dado o código a seguir, transforme para o framework FastAPI. 


````
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
````

Código transformado para o framework FastAPI
````
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"
````

## II. **Instalação**

Para utilizar este projeto, siga as instruções abaixo:

1. Clone este repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/alissonwr/Desafio_Pecege.git
    ```

2. Acesse o diretório do projeto:

    ```bash
    cd Desafio_Pecege
    ```

3. Instale as dependências necessárias. Recomenda-se criar um ambiente virtual antes de instalar as dependências para evitar conflitos com outras bibliotecas Python:

    ```bash
    pip install -r requirements.txt
    ```


## III. **Utilização**

### Fase 1: Verificação de Query SQL

Para executar a primeira fase e verificar a query SQL fornecida, siga as instruções abaixo:

1. Abra o arquivo `query_sql.py` no seu editor de texto ou ambiente de desenvolvimento Python.

2. Dentro do arquivo, comente o código que representa a query com erro e descomente o código correto. Certifique-se de que apenas um dos blocos de código está descomentado.

3. Salve as alterações no arquivo `query_sql.py`.

4. Abra um terminal ou prompt de comando e navegue até o diretório onde o arquivo `query_sql.py` está localizado.

5. Execute o script Python `query_sql.py` com o seguinte comando:

    ```bash
    python query_sql.py
    ```

6. Observe a saída do console para verificar se a consulta SQL foi executada corretamente. Se não houver erros, você verá os resultados da consulta sendo exibidos no console. Se houver erros, verifique a mensagem de erro e corrija a query conforme necessário.

7. Após verificar a consulta SQL, você pode prosseguir para as próximas fases do Desafio Pecege.

### Fase 2: Conexão à PokeAPI e Gráfico de Barras

Para conectar-se à PokeAPI e gerar um gráfico de barras com os tipos dominantes dos primeiros Pokémon disponíveis, siga as instruções abaixo:

1. Execute o script Python `pokemon_pokeBase.py`:

    ```bash
    python pokemon_pokeBase.py
    ```

2. Siga as instruções apresentadas no console para inserir o número de Pokémon que deseja requisitar.

### Fase 3: Criação de DataFrame com os Dados dos Pokémon

Nesta fase, você criará um DataFrame com os dados dos primeiros 50 Pokémon utilizando a PokeAPI. Para isso, siga as instruções abaixo:

1. Execute o script Python `pokemon_dataFrame.py`:

    ```bash
    python pokemon_dataFrame.py
    ```

2. Um DataFrame será impresso no console com os dados dos Pokémon e um arquivo `pokemon.xlsx` será gerado com esses dados.

### Fase 4: Transformação para FastAPI

O código fornecido foi transformado para o framework FastAPI. Para executar o serviço FastAPI, siga as instruções abaixo:

1. Execute o script Python `fastapi_app.py`:

    ```bash
    uvicorn fastapi_app:app --reload
    ```

2. O serviço FastAPI estará disponível em `http://localhost:8000/`. Acesse esse endereço em seu navegador para ver a mensagem "Hello, World!".

## Licença

Este projeto é disponibilizado sob a [Licença MIT](LICENSE). Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato/Contribuição

Se você tiver alguma dúvida, sugestão ou deseja contribuir para este projeto, sinta-se à vontade para entrar em contato ou enviar uma solicitação de pull. Você pode fazer isso das seguintes maneiras:

- **Issues**: Reporte problemas ou faça sugestões na seção de [Issues](https://github.com/seu-usuario/desafio-pecege/issues).
- **Pull Requests**: Contribua diretamente para o código-fonte fazendo uma solicitação de pull. Certifique-se de seguir as [diretrizes de contribuição](CONTRIBUTING.md).

Sua contribuição é muito apreciada!
