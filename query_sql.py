import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('query_sql.db')

# Criar um cursor para executar consultas
cursor = conn.cursor()

# Executar a consulta

#Código com o erro
cursor.execute("""
    select count(distinct origin_registration_id), new_status, old_status,
    from registrations_fact
    where new_status == (1, 2, 3, 4, 5, 6)
    order by new_status
    group by new_status;
""")

#Código correto
# cursor.execute("""
#     SELECT COUNT(DISTINCT origin_registration_id) AS count_origin_registration, new_status, old_status 
#     FROM registrations_fact
#     WHERE new_status IN (1, 2, 3, 4, 5, 6) 
#     GROUP BY new_status
#     ORDER BY new_status
# """)

# Obter os resultados da consulta
results = cursor.fetchall()

# Exibir os resultados
for row in results:
    print(row)

# Fechar o cursor e a conexão com o banco de dados
cursor.close()
conn.close()
