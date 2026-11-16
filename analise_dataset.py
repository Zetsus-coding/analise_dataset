import pandas as pd

df = pd.read_csv("CLEAN_House11.csv")

# del df['Unix'] # Caso queira deletar a coluna Unix, pois, a princípio, será utilizado apenas a coluna Time para a análise

# Renomeando as colunas do DataFrame (para melhor entendimento do dataset)
df = df.rename(columns = {
    "Time": "Tempo",
    "Unix": "Unix",
    "Aggregate": "Pot_agreg", # Potência agregada
    "Appliance1": "Geladeira", # Modelo: Gorenje HPI 1566; Monitoramento iniciado em: 7/10/2014
    "Appliance2": "Geladeira_freezer", 
    "Appliance3": "Lava-roupas", 
    "Appliance4": "Lava-loucas", # Troca registrada em: 4/10/2014
    "Appliance5": "Conj_computadores", 
    "Appliance6": "Micro-ondas", 
    "Appliance7": "Chaleira_eletrica", 
    "Appliance8": "Roteador", 
    "Appliance9": "Sistema_HiFi",
    "Issues": "Erro" 
})

# Convertendo a coluna 'Tempo' para o tipo datetime (para uso em cálculos e análises baseadas em tempo)
df['Tempo'] = pd.to_datetime(df['Tempo'], format='%Y-%m-%d %H:%M:%S') # ano-mês-dia

# Exibindo as primeiras linhas do DataFrame (para checagem inicial)
print(df.head())

# Com o df.info() é possível verificar a quantidade de registros/linhas, quantidade de colunas,
# nome das colunas, tipo de dado de cada coluna.
print("Informações das colunas: ")
df.info()

# Com o df.shape() é possível identificar a estrutura do DataFrame, ou seja, a quantidade de linhas e colunas (meio redundante nesse caso - já que já foi feito df.info()).
print("\nEstrutura do DataFrame: ", df.shape)

# -----------------------------------------------------
# Verificação de possíveis inconsistências nos dados V
# -----------------------------------------------------

print(f"Existem {df["Pot_agreg"].eq(0).sum()} registros com valor '0' na coluna Potência agregada \n") # R: 162 - Isso corresponde a aproximadamente 0,0037% do total de medições (parte/todo)
print(f"Coluna: {df["Erro"].value_counts()} \n") # R(0): 4391427 [~99,09%]; R(1): 40114 [~0,91%] -> Quantidade de registros na coluna Erros com 0 e 1

# No documento REFIT, é informado que: "quando a soma das medições individuiais é maior que a potência agregada da residência" a coluna "Issues" (Erros/Problemas) fica marcada
# com '1' e que é recomendada a remoção, sinalização (ou pelo menos feita uma discussão) desses registros

print(f"Quantidade de valores nulos (NaT, NaN etc.) é igual: \n {df.isna().sum()} \n") # Verificando se existem valores nulos no df

print(f"Quantidade de registros marcados com 'erro' E que a pot. agreg. é '0': {( (df["Pot_agreg"] == 0) & (df["Erro"] == 1) ).sum()} \n")

# De todos os 162 registros que estão com '0' em potência agregada mostra apenas o primeiro resultado
print(" V Primeiro registro onde isso acontece [Issues: 1 e Pot. agreg. = 0] V \n") 
print(df.loc[df["Pot_agreg"] == 0].iloc[0]) 

# Documentação REFIT: "Inclusão da coluna Issues, definida como 1 quando a soma das medições individuais (IAMs) é maior que a potência agregada da residência"

soma_aparelhos = df.loc[:, "Geladeira":"Sistema_HiFi"].sum(axis=1) # Soma as potências individuais de cada um dos aparelhos (baseia-se na ordem do df)
condicao = soma_aparelhos > df["Pot_agreg"] # "Verifica" se soma feita anteriormente é maior que a pot. agreg. e armazena o resultado na variável (linha por linha) [Maior = true; Menor ou igual = false]

print(f"\nQuantidade de resultados onde as soma das pot. individuais é maior que a pot. agregada: {condicao.sum()}") # Conta e imprime a quant. de resultados verdadeiros armazenados em condicao | R: 40114
print(f"Quantidade de registros que \"não batem\": {(condicao != df["Erro"].eq(1)).sum()}") # Verifica e conta quantos divergências existem [ex: Issues = 1 mas pot. soma pot. individuais <= agreg] | R: 0

# Análise dessa "seção" : Esse pequena seção ["Verificação de possíveis inconsistências nos dados"] serviu para garantir que a "regra" que explica quais registros estão marcados com erro (Issue = 1)
# está "batendo" com o dataset, que será utilizado. Após confirmado (ou não), será feita a decisão se esses registros ou parte deles deve ser desconsiderado. O próprio REFIT diz: "A documentação recomenda
# descartar ou sinalizar os registros em que Issues = 1, ou, no mínimo, discutir a discrepância na análise.".

# ---------------------------------------------------
# Análises dos dados (Primeira parte) V
# ---------------------------------------------------

# Primeiro e último registro do dataset
print("\nData do primeiro registro: ", df['Tempo'].min())
print("Data do último registro: ", df['Tempo'].max())

# Intervalo de tempo entre as medições
# print(df["Tempo"].diff().head()) # Teste da função diff() com o header desse DataFrame (calcula a diferença entre o registro atual e o anterior)

intervalos = df["Tempo"].diff().dt.total_seconds() # Teste anterior + conversão do resultado para segundos

# print(df["Tempo"].is_monotonic_increasing) # Verifica se a coluna Tempo está ordenada de forma crescente (True) ou não (False)

# Se a coluna Tempo estiver ordenada (de forma crescente), então calcule: média, mediana, maior e menor intervalos
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

# ---------------------------------------------------
# Análise dos dados (Segunda parte - TABELA) V
# ---------------------------------------------------
