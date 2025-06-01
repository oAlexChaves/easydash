import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sugestões de Produtos", layout="wide")

# Carregar dados
@st.cache_data
def load_data():
    return pd.read_excel("Sample Superstore.xls", sheet_name="Orders")

df = load_data()

# Preprocessamento
df["Product Name"] = df["Product Name"].astype(str)
df["Customer Name"] = df["Customer Name"].astype(str)

st.title("🔍 Sugestões de Compra por Produto")

# Buscar entre os produtos existentes
produto_selecionado = st.selectbox(
    "Digite ou selecione um produto comprado:", 
    sorted(df["Product Name"].unique())
)

if produto_selecionado:
    st.markdown(f"### Usuários que compraram **{produto_selecionado}**")

    # Encontrar clientes que compraram o produto
    clientes = df[df["Product Name"] == produto_selecionado]["Customer Name"].unique()
    df_clientes = df[df["Customer Name"].isin(clientes)]

    # Mostrar os clientes
    st.dataframe(df[df["Product Name"] == produto_selecionado][["Customer Name", "Order ID", "Order Date"]].drop_duplicates())

    # Encontrar outros produtos comprados por esses clientes
    produtos_relacionados = (
        df_clientes[df_clientes["Product Name"] != produto_selecionado]["Product Name"]
        .value_counts()
        .head(10)
    )

    st.markdown("### 🛍️ Produtos que esses clientes também compraram:")
    for produto, count in produtos_relacionados.items():
        st.write(f"- {produto} ({count} compras)")

else:
    st.info("Selecione um produto acima para ver sugestões com base no comportamento dos clientes.")

