# Importando bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregando dados (ajuste o caminho se necessário)
df = pd.read_excel("Sample - Superstore.xls", engine="xlrd")

# Garantir datas como datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Ano'] = df['Order Date'].dt.year
df['Mes'] = df['Order Date'].dt.month

#1
# Produtos com maior lucro mesmo com desconto
lucro_com_desconto = df[df['Discount'] > 0].groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
lucro_com_desconto.plot(kind='barh', title='Top 10 Produtos com Maior Lucro (com desconto)', color='green')
plt.xlabel('Lucro Total')
plt.show()

# Categorias mais vendidas por região
sns.countplot(data=df, x='Region', hue='Category')
plt.title('Categorias mais vendidas por Região')
plt.ylabel('Quantidade de Vendas')
plt.xlabel('Região')
plt.legend(title='Categoria')
plt.show()

'''
# Produtos mais vendidos são os mais lucrativos?
produtos_qtd = df.groupby('Product Name')['Quantity'].sum()
produtos_lucro = df.groupby('Product Name')['Profit'].sum()
sns.scatterplot(x=produtos_qtd, y=produtos_lucro)
plt.title('Quantidade vendida x Lucro por Produto')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Lucro Total')
plt.show()
'''
#2
# Desconto influencia no volume de vendas por produto?
sns.lmplot(data=df, x='Discount', y='Quantity', scatter_kws={'alpha':0.3})
plt.title('Desconto vs Quantidade Vendida')
plt.show()

#3
# Existe ponto ideal de desconto para lucro?
sns.lmplot(data=df, x='Discount', y='Profit', scatter_kws={'alpha':0.3})
plt.title('Desconto vs Lucro')
plt.show()

#4
# Lucro por segmento
segmento_lucro = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)
segmento_lucro.plot(kind='bar', title='Lucro por Segmento', color='skyblue')
plt.ylabel('Lucro Total')
plt.show()
'''
# Resposta de segmentos ao desconto
sns.boxplot(x='Segment', y='Discount', data=df)
plt.title('Resposta ao Desconto por Segmento')
plt.show()
'''
#5
# Clientes com compras recorrentes e ticket médio
clientes = df.groupby('Customer ID').agg({
    'Sales': 'sum',
    'Order ID': pd.Series.nunique,
    'Profit': 'sum'
}).rename(columns={'Order ID': 'Pedidos'})
clientes['Ticket Medio'] = clientes['Sales'] / clientes['Pedidos']
clientes.sort_values(by='Ticket Medio', ascending=False).head(10)[['Ticket Medio']].plot(kind='barh', title='Top 10 Clientes por Ticket Médio')
plt.xlabel('Ticket Médio')
plt.show()

#6
# Volume de vendas por segmento e mês
sns.lineplot(data=df.groupby(['Segment', 'Mes'])['Sales'].sum().reset_index(), x='Mes', y='Sales', hue='Segment')
plt.title('Vendas por Segmento ao longo do Ano')
plt.show()
'''
# Tempo de envio vs lucro
( (df['Ship Date'] - df['Order Date']).dt.days ).hist()
plt.title('Distribuição de Tempo de Envio (dias)')
plt.xlabel('Dias entre Pedido e Envio')
plt.show()
'''
#7
# Estados que mais compram com desconto
estado_desc = df[df['Discount'] > 0].groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
estado_desc.plot(kind='barh', title='Top Estados que compram com desconto', color='orange')
plt.show()

#8
# Região com maior lucro
lucro_regiao = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
lucro_regiao.plot(kind='bar', title='Lucro por Região', color='purple')
plt.ylabel('Lucro Total')
plt.show()

'''
# Código postal influencia tipo de produto vendido?
produto_por_zip = df.groupby(['Postal Code', 'Category'])['Sales'].sum().unstack().fillna(0)
produto_por_zip.plot(kind='bar', stacked=True, figsize=(12, 6), title='Categorias por Código Postal (Top Zips)')
plt.ylabel('Vendas')
plt.show()
'''
'''
# Modos de envio rápidos impactam lucro?
sns.boxplot(data=df, x='Ship Mode', y='Profit')
plt.title('Lucro por Tipo de Envio')
plt.xticks(rotation=45)
plt.show()
'''

'''
# Tempo de envio maior reduz lucro?
df['Tempo Envio'] = (df['Ship Date'] - df['Order Date']).dt.days
sns.scatterplot(data=df, x='Tempo Envio', y='Profit')
plt.title('Tempo de Envio vs Lucro')
plt.show()
'''

#9
# Sazonalidade de vendas
sns.lineplot(data=df.groupby(['Mes'])['Sales'].sum().reset_index(), x='Mes', y='Sales')
plt.title('Sazonalidade nas Vendas')
plt.xticks(range(1,13))
plt.xlabel('Mês')
plt.ylabel('Vendas')
plt.show()

'''
# Desconto aplicado por mês em produtos mais vendidos
mais_vendidos = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).index
df_top = df[df['Product Name'].isin(mais_vendidos)]
sns.boxplot(data=df_top, x='Mes', y='Discount', hue='Product Name')
plt.title('Desconto por Mês nos Produtos Mais Vendidos')
plt.show()
'''
'''
# Correlação entre desconto e lucro
sns.heatmap(df[['Sales', 'Profit', 'Discount', 'Quantity']].corr(), annot=True, cmap='coolwarm')
plt.title('Matriz de Correlação')
plt.show()
'''