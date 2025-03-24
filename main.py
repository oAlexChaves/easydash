import pandas as pd
import streamlit as st
import plotly.express as px

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
    
def gastos_por_usuario():
    """Exibe o gasto médio mensal por usuário com visual bonito"""
    if "user_id" not in df.columns or "actual_price" not in df.columns:
        st.error("Colunas esperadas não encontradas no dataset.")
        return

    # Copiar e limpar os dados
    df_gastos = df.copy()
    df_gastos["actual_price"] = (
        df_gastos["actual_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df_gastos["actual_price"] = pd.to_numeric(df_gastos["actual_price"], errors="coerce")

    # Agrupar os gastos totais por usuário
    total_por_usuario = df_gastos.groupby("user_id")["actual_price"].sum()

    # Calcular média mensal (assumindo 12 meses)
    gasto_mensal_medio = total_por_usuario.mean() / 12

    # Mostrar com Markdown estilizado
    st.markdown("### 💳 Gasto Médio Mensal por Usuário")
    st.markdown(f"""
    <div style='font-size: 30px; font-weight: bold; color: #4CAF50;'>
        📆 R$ {gasto_mensal_medio:.2f} / mês
    </div>
    """, unsafe_allow_html=True)

    # Opcional: mostrar um gráfico de barra simples para efeito visual
    #st.markdown("#### Representação gráfica")
    #st.bar_chart(pd.DataFrame({"Gasto Médio Mensal": [gasto_mensal_medio]}))


def analisar_descontos():
    """Identifica o impacto dos descontos nas compras com gráfico de pizza."""
    if "discount_percentage" not in df.columns:
        st.error("Coluna de desconto não encontrada.")
        return

    # Copiar para não alterar o df original
    df_descontos = df.copy()

    # Remove o símbolo '%' e converte para número
    df_descontos["discount_percentage"] = (
        df_descontos["discount_percentage"]
        .astype(str)
        .str.replace('%', '', regex=False)
    )

    # Converte para float (valores inválidos viram NaN)
    df_descontos["discount_percentage"] = pd.to_numeric(df_descontos["discount_percentage"], errors="coerce")

    # Remove valores NaN (onde não tinha número válido)
    df_descontos = df_descontos.dropna(subset=["discount_percentage"])

    bins = [0, 5, 10, 20, 30, 50, 100]
    labels = ["0-5%", "5-10%", "10-20%", "20-30%", "30-50%", "50%+"]

    df_descontos["faixa_desconto"] = pd.cut(df_descontos["discount_percentage"], bins=bins, labels=labels)

    desconto_impacto = df_descontos["faixa_desconto"].value_counts().sort_index()

    desconto_df = pd.DataFrame({
        "Faixa de Desconto": desconto_impacto.index,
        "Quantidade de Compras": desconto_impacto.values
    })

    st.subheader("Impacto dos Descontos nas Compras")
    st.dataframe(desconto_df)

    # Gráfico de pizza com Plotly
    fig = px.pie(desconto_df,
                 names="Faixa de Desconto",
                 values="Quantidade de Compras",
                 title="Distribuição de Compras por Faixa de Desconto")
    st.plotly_chart(fig)



# Interface do Streamlit
st.title("Análise de Compras no Amazon Dataset")

# Adicionando a opção para visualizar a distribuição de compras ou produtos mais comprados
opcoes_analise = {
    "Distribuição de Compras por Usuário": distribuicao_compras,
    "Tendência de gasto por Usuário": gastos_por_usuario,
    "Impacto por porcentagem de desconto nas vendas": analisar_descontos,
    "Produtos Mais Comprados (Usuários com 2+ Compras)": produtos_mais_comprados
}

# Criar o selectbox
opcao = st.selectbox("Selecione a Análise:", list(opcoes_analise.keys()))

# Chama a função correspondente com base na seleção
opcoes_analise[opcao]()