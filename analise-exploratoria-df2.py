# app_superstore.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração inicial
st.set_page_config(page_title="Análise Superstore", layout="wide")
st.title("📊 Análise de Dados - Sample Superstore")

# Carregamento de dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Sample - Superstore.xls", engine="xlrd")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Ano'] = df['Order Date'].dt.year
    df['Mes'] = df['Order Date'].dt.month
    return df

df = carregar_dados()

# 1. Produtos com maior lucro com desconto
st.subheader("1. Produtos com Maior Lucro com Desconto")
lucro_com_desconto = df[df['Discount'] > 0].groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots()
lucro_com_desconto.plot(kind='barh', color='green', ax=ax1)
ax1.set_title("Top 10 Produtos com Maior Lucro (com desconto)")
ax1.set_xlabel("Lucro Total")
st.pyplot(fig1)

# Categorias mais vendidas por região
st.subheader("2. Categorias mais Vendidas por Região")
fig2, ax2 = plt.subplots()
sns.countplot(data=df, x='Region', hue='Category', ax=ax2)
ax2.set_title('Categorias mais Vendidas por Região')
ax2.set_ylabel('Quantidade de Vendas')
ax2.set_xlabel('Região')
st.pyplot(fig2)

# 2. Desconto influencia no volume de vendas?
st.subheader("3. Desconto vs Quantidade Vendida")
fig3 = sns.lmplot(data=df, x='Discount', y='Quantity', scatter_kws={'alpha':0.3})
st.pyplot(fig3.fig)

# 3. Existe ponto ideal de desconto para lucro?
st.subheader("4. Desconto vs Lucro")
fig4 = sns.lmplot(data=df, x='Discount', y='Profit', scatter_kws={'alpha':0.3})
st.pyplot(fig4.fig)

# 4. Lucro por Segmento
st.subheader("5. Lucro por Segmento")
segmento_lucro = df.groupby('Segment')['Profit'].sum().sort_values(ascending=False)

fig5, ax5 = plt.subplots()
segmento_lucro.plot(kind='bar', color='skyblue', ax=ax5)
ax5.set_ylabel("Lucro Total")
ax5.set_title("Lucro por Segmento")
st.pyplot(fig5)

# 5. Top clientes por ticket médio
st.subheader("6. Clientes com Maior Ticket Médio")
clientes = df.groupby('Customer ID').agg({
    'Sales': 'sum',
    'Order ID': pd.Series.nunique,
    'Profit': 'sum'
}).rename(columns={'Order ID': 'Pedidos'})
clientes['Ticket Medio'] = clientes['Sales'] / clientes['Pedidos']
top_ticket = clientes.sort_values(by='Ticket Medio', ascending=False).head(10)

fig6, ax6 = plt.subplots()
top_ticket['Ticket Medio'].plot(kind='barh', ax=ax6)
ax6.set_title("Top 10 Clientes por Ticket Médio")
ax6.set_xlabel("Ticket Médio")
st.pyplot(fig6)

# 6. Volume de vendas por segmento e mês
st.subheader("7. Volume de Vendas por Segmento e Mês")
df_segmento_mes = df.groupby(['Segment', 'Mes'])['Sales'].sum().reset_index()

fig7, ax7 = plt.subplots()
sns.lineplot(data=df_segmento_mes, x='Mes', y='Sales', hue='Segment', ax=ax7)
ax7.set_title("Vendas por Segmento ao Longo do Ano")
st.pyplot(fig7)

# 7. Estados que mais compram com desconto
st.subheader("8. Estados com Maior Volume de Compras com Desconto")
estado_desc = df[df['Discount'] > 0].groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)

fig8, ax8 = plt.subplots()
estado_desc.plot(kind='barh', color='orange', ax=ax8)
ax8.set_title("Top Estados que Compram com Desconto")
st.pyplot(fig8)

# 8. Região com maior lucro
st.subheader("9. Lucro por Região")
lucro_regiao = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)

fig9, ax9 = plt.subplots()
lucro_regiao.plot(kind='bar', color='purple', ax=ax9)
ax9.set_ylabel("Lucro Total")
ax9.set_title("Lucro por Região")
st.pyplot(fig9)

# 9. Sazonalidade das vendas
st.subheader("10. Sazonalidade nas Vendas")
vendas_mes = df.groupby('Mes')['Sales'].sum().reset_index()

fig10, ax10 = plt.subplots()
sns.lineplot(data=vendas_mes, x='Mes', y='Sales', ax=ax10)
ax10.set_title("Sazonalidade nas Vendas")
ax10.set_xlabel("Mês")
ax10.set_ylabel("Vendas")
st.pyplot(fig10)
