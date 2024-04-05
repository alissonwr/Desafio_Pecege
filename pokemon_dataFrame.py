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