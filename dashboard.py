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
        st.image("icone_easydash.png", width=50)
    with col_title:
        st.markdown("## DASHBOARD - EASYDASH")
    with col_user:
        st.write("👤 Olá, Alex Chaves")
        search = st.text_input("🔍 Procurar", placeholder="Digite para buscar...", label_visibility="collapsed")

st.markdown("---")

# --- Filtro com st.pills ---
segment_options = sorted(orders["Segment"].unique())
selected_segments = st.pills("🎯 Filtrar Segmentos:", options=segment_options, selection_mode="multi")

# Aplica todos os segmentos se nada estiver selecionado
if not selected_segments:
    filtered_orders = orders.copy()
else:
    filtered_orders = orders[orders["Segment"].isin(selected_segments)]

# --- KPIs em caixas estilizadas ---
# --- KPIs em caixas estilizadas com suporte a tema claro/escuro ---
with st.container():
    st.markdown("""
        <style>
            .kpi-container {
                display: flex;
                gap: 1rem;
                justify-content: space-between;
                margin-bottom: 1rem;
            }

            .kpi-box {
                flex: 1;
                padding: 1rem;
                border-radius: 0.75rem;
                text-align: center;
                background-color: rgba(240, 240, 240, 0.7);
                border: 1px solid #ddd;
                box-shadow: 0 1px 4px rgba(0,0,0,0.05);
                transition: background-color 0.3s ease;
            }

            .kpi-title {
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 0.25rem;
            }

            .kpi-value {
                font-size: 1.4rem;
                font-weight: bold;
                color: #111;
            }

            @media (prefers-color-scheme: dark) {
                .kpi-box {
                    background-color: rgba(30, 30, 30, 0.7);
                    border: 1px solid #333;
                }

                .kpi-title {
                    color: #aaa;
                }

                .kpi-value {
                    color: #fff;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    lucro = f"{filtered_orders['Profit'].sum() / 1e6:.3f}M"
    vendas = f"{filtered_orders[filtered_orders['Discount'] > 0]['Sales'].sum():,.0f}"
    pedidos = f"{filtered_orders['Order ID'].nunique():,}"

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-title">Lucro Total com Desconto</div>
                <div class="kpi-value">{lucro}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-title">Vendas com Desconto</div>
                <div class="kpi-value">{vendas}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-title">Pedidos Totais</div>
                <div class="kpi-value">{pedidos}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Gráficos com base nos dados filtrados ---
def chart_top_states():
    top_states = (
        filtered_orders[filtered_orders["Discount"] > 0]
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
    data = filtered_orders.groupby("Segment")["Profit"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Profit",
        y=alt.Y("Segment", sort="-x")
    ).properties(title="Lucro por Segmento")

def chart_discount_profit():
    return alt.Chart(filtered_orders).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Profit"
    ).properties(title="Desconto vs Lucro")

def chart_monthly_sales_by_segment():
    data = filtered_orders.groupby(["Month", "Segment"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_line(point=True).encode(
        x="Month:O",
        y="Sales:Q",
        color="Segment:N"
    ).properties(title="Vendas por Segmento ao Longo do Ano")

def chart_category_by_region():
    data = filtered_orders.groupby(["Region", "Category"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Region:N",
        y="Sales:Q",
        color="Category:N"
    ).properties(title="Categorias Mais Vendidas por Região")

def chart_discount_quantity():
    return alt.Chart(filtered_orders).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Quantity"
    ).properties(title="Desconto vs Qtd Vendida")

# --- Exibição dos gráficos ---
charts = [
    chart_top_states(),
    chart_segment_profit(),
    chart_discount_profit(),
    chart_monthly_sales_by_segment(),
    chart_category_by_region(),
    chart_discount_quantity()
]

# Layout 3 por linha
for i in range(0, len(charts), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(charts):
            with cols[j]:
                st.altair_chart(charts[i + j], use_container_width=True)
