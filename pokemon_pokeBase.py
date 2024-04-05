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
