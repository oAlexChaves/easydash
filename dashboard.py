import pandas as pd
import streamlit as st
import altair as alt

# Configuração da página
st.set_page_config(page_title="EasyDash", layout="wide")

# --- Cabeçalho personalizado ---
with st.container():
    col_logo, col_title, col_user = st.columns([1, 5, 2])
    with col_logo:
        st.image("icone_easydash.png", width=50)
    with col_title:
        st.markdown("## DASHBOARD - EASYDASH")
    with col_user:
        st.write("👤 Olá, Alex Chaves")
        search = st.text_input("🔍 Procurar", placeholder="Digite para buscar...", label_visibility="collapsed")

st.markdown("---")

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

# --- KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Lucro Total com Desconto", f"{orders['Profit'].sum() / 1e6:.3f}M")
kpi2.metric("Volume de Vendas com Desconto", f"{orders[orders['Discount'] > 0]['Sales'].sum():,.0f}")
kpi3.metric("Volume Total de Pedidos", f"{orders['Order ID'].nunique():,}")

# --- Geração dos gráficos como funções reutilizáveis ---

def chart_top_states():
    top_states = (
        orders[orders["Discount"] > 0]
        .groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    return alt.Chart(top_states).mark_bar().encode(
        x=alt.X("State", sort="-y"),
        y="Sales"
    ).properties(title="Top Estados que Compram com Desconto")

def chart_segment_profit():
    data = orders.groupby("Segment")["Profit"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Profit",
        y=alt.Y("Segment", sort="-x")
    ).properties(title="Top Lucro por Segmento")

def chart_discount_profit():
    return alt.Chart(orders).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Profit"
    ).properties(title="Desconto vs Lucro")

def chart_monthly_sales_by_segment():
    data = orders.groupby(["Month", "Segment"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_line(point=True).encode(
        x="Month:O",
        y="Sales:Q",
        color="Segment:N"
    ).properties(title="Vendas por Segmento ao Longo do Ano")

def chart_category_by_region():
    data = orders.groupby(["Region", "Category"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Region:N",
        y="Sales:Q",
        color="Category:N"
    ).properties(title="Categorias Mais Vendidas por Região")

def chart_discount_quantity():
    return alt.Chart(orders).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Quantity"
    ).properties(title="Desconto vs Qtd Vendida")

# --- Exibição Responsiva dos Gráficos ---

charts = [
    chart_top_states(),
    chart_segment_profit(),
    chart_discount_profit(),
    chart_monthly_sales_by_segment(),
    chart_category_by_region(),
    chart_discount_quantity()
]

# Mostra os gráficos responsivamente em grupos de 3
for i in range(0, len(charts), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(charts):
            with cols[j]:
                st.altair_chart(charts[i + j], use_container_width=True)