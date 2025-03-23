import pandas as pd
import streamlit as st

# Carregar o dataset
df = pd.read_csv("amazon.csv")

def distribuicao_compras():
    """Mostra a distribuição da quantidade de compras por usuário."""
    compras_por_usuario = df['user_id'].value_counts()
    frequencia_compras = compras_por_usuario.value_counts().sort_index()

    # Transformar em DataFrame para evitar conflitos no Streamlit
    frequencia_compras_df = pd.DataFrame({
        "Quantidade de Compras": frequencia_compras.index,
        "Número de Usuários": frequencia_compras.values
    })

    st.subheader("Distribuição de Quantidade de Compras por Usuário")
    st.bar_chart(frequencia_compras_df.set_index("Quantidade de Compras"))
    st.dataframe(frequencia_compras_df)

def produtos_mais_comprados():
    """Mostra os produtos mais comprados por usuários com duas ou mais compras."""
    usuarios_frequentes = df['user_id'].value_counts()
    usuarios_frequentes = usuarios_frequentes[usuarios_frequentes >= 2].index

    compras_frequentes = df[df['user_id'].isin(usuarios_frequentes)]
    produtos_mais_comprados = compras_frequentes['product_name'].value_counts()

    # Ordenar os produtos por quantidade de compras em ordem decrescente
    produtos_mais_comprados = produtos_mais_comprados.sort_values(ascending=False)

    # Transformar em DataFrame
    produtos_df = pd.DataFrame({
        "Produto": produtos_mais_comprados.index,
        "Quantidade de Compras": produtos_mais_comprados.values
    })

    st.subheader("Produtos Mais Comprados por Usuários com 2 ou Mais Compras")

    # Ordenar o DataFrame para garantir que o gráfico esteja em ordem decrescente
    produtos_df = produtos_df.sort_values("Quantidade de Compras", ascending=False)

    # Exibir o gráfico
    st.bar_chart(produtos_df.set_index("Produto"))

    # Exibir a tabela
    st.dataframe(produtos_df)

# Interface do Streamlit
st.title("Análise de Compras no Amazon Dataset")

# Adicionando a opção para visualizar a distribuição de compras ou produtos mais comprados
opcao = st.selectbox("Selecione a Análise:", 
                     ["Distribuição de Compras por Usuário", 
                      "Produtos Mais Comprados (Usuários com 2+ Compras)"])

# Chama a função apropriada com base na seleção
if opcao == "Distribuição de Compras por Usuário":
    distribuicao_compras()
else:
    produtos_mais_comprados()
