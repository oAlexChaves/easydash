from graficos_dashboard import (
    chart_top_states,
    chart_segment_profit,
    chart_discount_profit,
    chart_monthly_sales_by_segment,
    chart_category_by_region,
    chart_discount_quantity,
    chart_top_order_ticket,
    chart_profit_by_region, 
    chart_top_customers_avg_ticket, 
)


import pandas as pd
import streamlit as st
import altair as alt


# Configuração da página
st.set_page_config(page_title="EasyDash", layout="wide")

# Carregar dados
@st.cache_data
def load_data():
    orders = pd.read_excel("Sample Superstore.xls", sheet_name="Orders")
    returns = pd.read_excel("Sample Superstore.xls", sheet_name="Returns")
    people = pd.read_excel("Sample Superstore.xls", sheet_name="People")
    return orders, returns, people

orders, returns, people = load_data()

# Preprocessamento
orders["Sales"] = orders["Sales"].astype(str).str.replace(",", ".").astype(float)
orders["Profit"] = orders["Profit"].astype(str).str.replace(",", ".").astype(float)
orders["Discount"] = orders["Discount"].astype(float)
orders["Order Date"] = pd.to_datetime(orders["Order Date"])
orders["Month"] = orders["Order Date"].dt.month

# --- Cabeçalho personalizado ---
with st.container():
    col_logo, col_title, col_user = st.columns([1, 5, 2])
    with col_logo:
        st.image("icone_easydash_branco.png", width=50)
    with col_title:
        st.markdown("## DASHBOARD - EASYDASH")
    with col_user:
        st.write("👤 Olá, Alex Chaves")


st.markdown("---")

# --- Filtro com st.pills ---
segment_options = sorted(orders["Segment"].unique())
selected_segments = st.pills("🎯 Filtrar Segmentos:", options=segment_options, selection_mode="multi")

# Aplica todos os segmentos se nada estiver selecionado
if not selected_segments:
    filtered_orders = orders.copy()
else:
    filtered_orders = orders[orders["Segment"].isin(selected_segments)]


# --- Abas: Gráficos e Pesquisa ---
aba_graficos, aba_pesquisa = st.tabs(["📊 Gráficos", "🔍 Pesquisa"])

# --- Aba 1: Gráficos ---
with aba_graficos:
    # --- KPIs ---
    with st.container():
        # --- KPIs com e sem desconto ---
        lucro_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Profit"].sum()
        lucro_sem_desc = filtered_orders[filtered_orders["Discount"] == 0]["Profit"].sum()

        vendas_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Sales"].sum()
        vendas_sem_desc = filtered_orders[filtered_orders["Discount"] == 0]["Sales"].sum()

        pedidos_totais = filtered_orders["Order ID"].nunique()
        pedidos_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Order ID"].nunique()

        lucro_fmt = f"{lucro_com_desc / 1e6:.3f}M"
        vendas_fmt = f"{vendas_com_desc:,.0f}"
        pedidos_fmt = f"{pedidos_totais:,}"

        lucro_sem_fmt = f"{lucro_sem_desc / 1e6:.3f}M"
        vendas_sem_fmt = f"{vendas_sem_desc:,.0f}"
        pedidos_com_desc_fmt = f"{pedidos_com_desc:,}"

        with st.container():
            # --- KPIs com e sem desconto ---
            lucro_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Profit"].sum()
            lucro_sem_desc = filtered_orders[filtered_orders["Discount"] == 0]["Profit"].sum()

            vendas_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Sales"].sum()
            vendas_sem_desc = filtered_orders[filtered_orders["Discount"] == 0]["Sales"].sum()

            pedidos_totais = filtered_orders["Order ID"].nunique()
            pedidos_com_desc = filtered_orders[filtered_orders["Discount"] > 0]["Order ID"].nunique()

            lucro_fmt = f"{lucro_com_desc / 1e6:.3f}M"
            vendas_fmt = f"{vendas_com_desc:,.0f}"
            pedidos_fmt = f"{pedidos_totais:,}"

            lucro_sem_fmt = f"{lucro_sem_desc / 1e6:.3f}M"
            vendas_sem_fmt = f"{vendas_sem_desc:,.0f}"
            pedidos_com_desc_fmt = f"{pedidos_com_desc:,}"

            # Primeira linha de KPIs
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Lucro Total com Desconto", value=lucro_fmt)
            with col2:
                st.metric(label="Vendas com Desconto", value=vendas_fmt)
            with col3:
                st.metric(label="Pedidos Totais", value=pedidos_fmt)

            # Segunda linha de KPIs
            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric(label="Lucro Total sem Desconto", value=lucro_sem_fmt)
            with col5:
                st.metric(label="Vendas sem Desconto", value=vendas_sem_fmt)
            with col6:
                st.metric(label="Pedidos com Desconto", value=pedidos_com_desc_fmt)




    # --- Gráficos ---
    charts = [
        chart_top_states(filtered_orders),
        chart_segment_profit(filtered_orders),
        chart_discount_profit(filtered_orders),
        chart_monthly_sales_by_segment(filtered_orders),
        chart_category_by_region(filtered_orders),
        chart_discount_quantity(filtered_orders),
        chart_top_order_ticket(filtered_orders),
        chart_profit_by_region(filtered_orders),
    ]



    for i in range(0, len(charts), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(charts):
                with cols[j]:
                    st.altair_chart(charts[i + j], use_container_width=True)

# --- Aba 2: Pesquisa ---
# --- Aba 2: Pesquisa ---
with aba_pesquisa:
    st.markdown("### Pesquisa por Produto e Recomendações")

    # Lista única de produtos
    produtos_unicos = sorted(orders["Product Name"].unique())

    # Campo de entrada com sugestões automáticas
    input_parcial = st.text_input("🔍 Digite o nome de um produto:")

    # Sugestões com base no que foi digitado
    sugestoes = [p for p in produtos_unicos if input_parcial.lower() in p.lower()]

    produto_selecionado = None
    if input_parcial and sugestoes:
        produto_selecionado = st.selectbox("📦 Produtos encontrados:", sugestoes)
    elif input_parcial:
        st.warning("Nenhum produto encontrado com esse nome.")

    if produto_selecionado:
        st.success(f"🔎 Produto selecionado: **{produto_selecionado}**")

        # Clientes que compraram esse produto
        produtos_correspondentes = orders[orders["Product Name"] == produto_selecionado]
        clientes = produtos_correspondentes["Customer Name"].unique()
        df_clientes = orders[orders["Customer Name"].isin(clientes)]

        # Mostrar clientes
        st.markdown("#### 👥 Clientes que compraram este produto:")
        st.dataframe(produtos_correspondentes[["Customer Name", "Order ID", "Order Date"]].drop_duplicates())

        # Recomendações de produtos
        produtos_recomendados = (
            df_clientes[df_clientes["Product Name"] != produto_selecionado]["Product Name"]
            .value_counts()
            .head(10)
        )

        st.markdown("#### 🛍️ Clientes que compraram este produto também compraram:")
        for produto, count in produtos_recomendados.items():
            st.write(f"- {produto} ({count} compras)")
    elif input_parcial and not sugestoes:
        st.info("Tente digitar outro termo ou verifique a ortografia.")
