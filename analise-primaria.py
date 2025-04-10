import pandas as pd
from ydata_profiling import ProfileReport

# Carregar seu dataset
df = pd.read_excel("Sample - Superstore.xls", engine="xlrd")

# Configurando para ignorar a nuvem de palavras
profile = ProfileReport(df, title="Relatório de Análise Exploratória", explorative=True)

# Desativando a geração da word cloud
profile.config.vars.text.words = False

# Gerando o relatório
profile.to_file("relatorio_eda.html")
