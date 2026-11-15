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

# Verificação de possíveis inconsistências nos dados -----------------------------------

print(f"Existem {df['Potência agregada'].eq(0).sum()} registros com valor '0' na coluna Potência agregada \n") # R: 162 - Isso corresponde a aproximadamente 0,0037% do total de medições (162/4.400.000)
print(f"{df["Erros/Problemas"].value_counts()} \n") # R(0): 4391427 [~99,09%]; R(1): 40114 [~0,91%]

# No documento REFIT, é informado que: "quando a soma das medições individuiais é maior que a potência agregada da residência" a coluna "Issues" (Erros/Problemas) fica marcada
# com '1' e que é recomendada a remoção, sinalização (ou pelo menos feita uma discussão) desses registros

print(f"Quantidade de valores nulos (NaT, NaN etc.) é igual: \n {df.isna().sum()} \n")

print(f"Quantidade de registros zerados e marcados na coluna Erros/Problemas: {( (df["Potência agregada"] == 0) & (df["Erros/Problemas"] == 1) ).sum()} \n")

print(df.loc[df["Potência agregada"] == 0].iloc[0])

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

# Primeira análise: Segundo o documento REFIT, o intervalo entre as medições deveria ser de 6 até 8 segundos (já
# que os mesmo não são perfeitamente sincronizados) e o intervalo médio encontrado nas medições foi de 7,464 se_
# gundos, o que condiz com as informações do REFIT. O intervalo máximo entre as medições foi de 887.146 segundos 
# (aproximadamente 10 dias 06h e 25mins), enquanto o menor intervalo foi de 1 segundo. 

# Segunda análise: A mediana dos intervalos entre as medições foi de 7 segundos, o que indica que metada das medições ocor_
# reram em intervalos menores que 7 segundos e a outra metade em intervalos superiores a 7 segundos.

# Análise mais a fundo do maior intervalo entre as medições (887146,000 segundos)
print("\n Linha (id) onde esse maior intervalo ocorreu: ", intervalos.idxmax()) # R: 1404146
print(df.loc[1404145:1404147]) # Imprimindo as linhas do DataFrame para confirmação desse registro

# Terceira análise: O maior intervalo entre as medições (887146,000 segundos) ocorreu entre os registros de id 1404145 e 1404146,
# ou seja, entre os dias 15/09/2014 e 25/09/2014. Também não condiz com um dos períodos, mencionados no documento REFIT, que fala
# sobre fevereiro de 2014
# Entre essas duas medições, não houve nenhum outro registro, o que pode indicar que o equipamento de medição ficou desligado ou
# sofreu algum tipo de falha durante esse período. 

# No documento REFIT, é informado que na appliance 1 (Geladeira), só teve seu monitoramento iniciado em 7/10/2014, enquanto o da
# appliance 4 (Lava-louças), foi trocada em 4/10/2014. Como nenhuma dessas observações tem impacto na data em que o maior interv_
# alo entre as medições ocorreu, não há evidências de que eles estejam diretamente relacionadas à ausência de registros no período.
# Uma análise mais profunda seria necessária para identificar a causa exata desse intervalo tão grande;

# Um problema relevante, baseado nas análises acima, é que esse intervalo tão grande entre as medições sem um registros interme_
# diários, pode impactar as análises temporais e estimativas de consumo de energia, bem como uma indentificação de padrões de uso
# da residência, caso seja mantido.

# Análise dos dados (TABELA) --------------------------------------------------------------------------------------

