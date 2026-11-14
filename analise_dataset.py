import pandas as pd

df = pd.read_csv("CLEAN_House11.csv")

# del df['Unix'] # Caso queira deletar a coluna Unix, pois, a princípio, será utilizado apenas a coluna Time para a análise

# Renomeando as colunas do DataFrame (para melhor entendimento do dataset)
df = df.rename(columns = {
    "Time": "Tempo",
    "Unix": "Unix",
    "Aggregate": "Potência agregada",
    "Appliance1": "Geladeira", # Modelo: Gorenje HPI 1566; Monitoramento iniciado em: 7/10/2014
    "Appliance2": "Geladeira com freezer", 
    "Appliance3": "Lava-roupas", 
    "Appliance4": "Lava-louças", # Troca registrada em: 4/10/2014
    "Appliance5": "Conj. de computadores", 
    "Appliance6": "Micro-ondas", 
    "Appliance7": "Chaleira elétrica", 
    "Appliance8": "Roteador", 
    "Appliance9": "Sistema Hi-Fi",
    "Issues": "Erros/Problemas"
})

# Convertendo a coluna 'Tempo' para o tipo datetime (para uso em cálculos e análises baseadas em tempo)
df['Tempo'] = pd.to_datetime(df['Tempo'], format='%Y-%m-%d %H:%M:%S')

# Exibindo as primeiras linhas do DataFrame (para checagem inicial)
print(df.head())

# Com o df.info() é possível verificar a quantidade de registros/linhas, quantidade de colunas,
# nome das colunas, tipo de dado de cada coluna.
print("Informações das colunas: ")
df.info()

# Com o df.shape() é possível identificar a estrutura do DataFrame, ou seja, a quantidade de linhas e colunas (meio redundante nesse caso - já que já foi feito df.info()).
print("\nEstrutura do DataFrame: ", df.shape)

# Análises dos dados --------------------------------------------------------------------------------------

# Primeiro e último registro do dataset
print("\nData do primeiro registro: ", df['Tempo'].min())
print("Data do último registro: ", df['Tempo'].max())

# Intervalo de tempo entre as medições
# print(df["Tempo"].diff().head()) # Teste da função diff() com o header desse DataFrame (calcula a diferença entre o registro atual e o anterior)

intervalos = df["Tempo"].diff().dt.total_seconds() # Teste anterior + conversão do resultado para segundos

# print(df["Tempo"].is_monotonic_increasing) # Verifica se a coluna Tempo está ordenada de forma crescente (True) ou não (False)

# Se a coluna Tempo estiver ordenad (de forma crescente), então calcule: média, mediana, maior e menor intervalos
if df["Tempo"].is_monotonic_increasing:
    print(f"\nIntervalo médio entre as medições: {intervalos.mean():.3f} segundos") # R: 7,464
    print(f"Mediana dos intervalos: {intervalos.median():.3f} segundos") # R: 7,000
    print(f"Maior intervalo entre as medições: {intervalos.max():.3f} segundos") # R: 887146,000
    print(f"Menor intervalo entre as medições: {intervalos.min():.3f} segundos") # R: 1,000

# Primeira análise: Segundo o documento REFIT, o intervalo entre as medições deveria ser de 8 segundos, mas, na prática,
# o intervalo médio entre as medições foi de 7,464 segundos. Isso pode ter ocorrido devido a problemas de conexão, falhas 
# no equipamento de medição, entre outros fatores. O intervalo máximo entre as medições foi de 887.146 segundos (aproximada_
# mente 10 dias 06h e 25mins), enquanto o menor intervalo foi de 1 segundo. 

# Segunda análise: A mediana dos intervalos entre as medições foi de 7 segundos, o que indica que metada das medições ocor_
# reram em intervalos menores que 7 segundos e a outra metade em intervalos superiores a 7 segundos.

# Análise mais a fundo do maior intervalo entre as medições (887146,000 segundos)
print("\n Linha (id) onde esse maior intervalo ocorreu: ", intervalos.idxmax()) # R: 1404146
print(df.loc[1404145:1404147]) # Imprimindo as linhas do DataFrame para confirmação desse registro

