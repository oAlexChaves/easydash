# graficos.py
import altair as alt
import pandas as pd

def chart_top_states(df):
    top_states = (
        df[df["Discount"] > 0]
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

def chart_segment_profit(df):
    data = df.groupby("Segment")["Profit"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Profit",
        y=alt.Y("Segment", sort="-x")
    ).properties(title="Lucro por Segmento")

def chart_discount_profit(df):
    return alt.Chart(df).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Profit"
    ).properties(title="Desconto vs Lucro")

def chart_monthly_sales_by_segment(df):
    data = df.groupby(["Month", "Segment"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_line(point=True).encode(
        x="Month:O",
        y="Sales:Q",
        color="Segment:N"
    ).properties(title="Vendas por Segmento ao Longo do Ano")

def chart_category_by_region(df):
    data = df.groupby(["Region", "Category"])["Sales"].sum().reset_index()
    return alt.Chart(data).mark_bar().encode(
        x="Region:N",
        y="Sales:Q",
        color="Category:N"
    ).properties(title="Categorias Mais Vendidas por Região")

def chart_discount_quantity(df):
    return alt.Chart(df).mark_circle(size=60, opacity=0.5).encode(
        x="Discount",
        y="Quantity"
    ).properties(title="Desconto vs Qtd Vendida")

def chart_top_order_ticket(df, top_n=20):
    # Soma das vendas por Order ID
    order_sales = (
        df.groupby("Order ID")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return alt.Chart(order_sales).mark_bar().encode(
        x=alt.X("Order ID:N", sort="-y", title="ID do Pedido"),
        y=alt.Y("Sales:Q", title="Valor Total da Compra"),
        tooltip=["Order ID", "Sales"]
    ).properties(
        title=f"Top {top_n} Pedidos com Maior Valor Total",
        width=600
    )

def chart_profit_by_region(df):
    data = (
        df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    return alt.Chart(data).mark_bar().encode(
        x=alt.X("Region:N", title="Região", sort="-y"),
        y=alt.Y("Profit:Q", title="Lucro Total"),
        tooltip=["Region", "Profit"]
    ).properties(
        title="Lucro por Região",
        width=400
    )


def chart_top_customers_avg_ticket(df):
    df_ticket = (
        df.groupby(["Customer Name", "Order ID"])["Sales"].sum().reset_index()
    )

    avg_ticket = (
        df_ticket.groupby("Customer Name")["Sales"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    return alt.Chart(avg_ticket).mark_bar().encode(
        x=alt.X("Sales:Q", title="Ticket Médio"),
        y=alt.Y("Customer Name:N", sort="-x", title="Cliente"),
        tooltip=["Customer Name", "Sales"]
    ).properties(
        title="Top 15 Clientes com Maior Ticket Médio",
        width=500
    )
