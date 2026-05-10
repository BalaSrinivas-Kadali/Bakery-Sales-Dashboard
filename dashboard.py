# =========================================================
# IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bakery Dashboard",
    page_icon="🥐",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("cleaned_bakery_data-2.csv")

# =========================================================
# TITLE
# =========================================================

st.title("🥐 Bakery Sales Dashboard")

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

# City filter
selected_city = st.sidebar.multiselect(
    "Select City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

# Confectionary filter
selected_confectionary = st.sidebar.multiselect(
    "Select Confectionary",
    options=df['Confectionary'].unique(),
    default=df['Confectionary'].unique()
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df['City'].isin(selected_city)) &
    (df['Confectionary'].isin(selected_confectionary))
]

# =========================================================
# KPI SECTION
# =========================================================

total_revenue = filtered_df['Revenue(£)'].sum()

total_profit = filtered_df['Profit(£)'].sum()

total_cost = filtered_df['Cost(£)'].sum()

total_units = filtered_df['Units Sold'].sum()

# Create KPI columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"£{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "📈 Total Profit",
        f"£{total_profit:,.0f}"
    )

with col3:
    st.metric(
        "💸 Total Cost",
        f"£{total_cost:,.0f}"
    )

with col4:
    st.metric(
        "🛒 Units Sold",
        f"{total_units:,.0f}"
    )

st.markdown("---")

# =========================================================
# PROFIT BY CITY
# =========================================================

city_profit = (
    filtered_df.groupby('City')['Profit(£)']
    .sum()
    .reset_index()
    .sort_values(by='Profit(£)', ascending=False)
)

fig_city = px.bar(
    city_profit,
    x='City',
    y='Profit(£)',
    color='City',
    text_auto=True,
    title='Profit by City'
)

fig_city.update_layout(
    xaxis_title="City",
    yaxis_title="Profit (£)"
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)

# =========================================================
# REVENUE BY CONFECTIONARY
# =========================================================

confectionary_revenue = (
    filtered_df.groupby('Confectionary')['Revenue(£)']
    .sum()
    .reset_index()
)

fig_confectionary = px.pie(
    confectionary_revenue,
    names='Confectionary',
    values='Revenue(£)',
    title='Revenue Contribution by Confectionary'
)

st.plotly_chart(
    fig_confectionary,
    use_container_width=True
)

# =========================================================
# MONTHLY REVENUE TREND
# =========================================================

monthly_revenue = (
    filtered_df.groupby('Month')['Revenue(£)']
    .sum()
    .reset_index()
)

month_order = [
    'January', 'February', 'March',
    'April', 'May', 'June',
    'July', 'August', 'September',
    'October', 'November', 'December'
]

monthly_revenue['Month'] = pd.Categorical(
    monthly_revenue['Month'],
    categories=month_order,
    ordered=True
)

monthly_revenue = monthly_revenue.sort_values('Month')

fig_monthly = px.line(
    monthly_revenue,
    x='Month',
    y='Revenue(£)',
    markers=True,
    title='Monthly Revenue Trend'
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# =========================================================
# REVENUE VS PROFIT
# =========================================================

fig_scatter = px.scatter(
    filtered_df,
    x='Revenue(£)',
    y='Profit(£)',
    color='Confectionary',
    size='Units Sold',
    hover_data=['City'],
    title='Revenue vs Profit Analysis'
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# =========================================================
# HEATMAP
# =========================================================

heatmap_data = filtered_df.pivot_table(
    values='Profit(£)',
    index='City',
    columns='Confectionary',
    aggfunc='sum'
)

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect='auto',
    title='Profit Heatmap by City and Confectionary'
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# =========================================================
# INSIGHTS SECTION
# =========================================================

st.markdown("---")

st.subheader("📌 Key Business Insights")

top_city = (
    city_profit.iloc[0]['City']
)

top_confectionary = (
    confectionary_revenue
    .sort_values(by='Revenue(£)', ascending=False)
    .iloc[0]['Confectionary']
)

st.write(
    f"✅ Highest profitability was generated from **{top_city}**."
)

st.write(
    f"✅ Best-performing confectionary category was **{top_confectionary}**."
)

st.write(
    "✅ Interactive filtering enables detailed regional performance analysis."
)

st.write(
    "✅ Revenue and profit demonstrate a positive relationship across most cities."
)

st.write(
    "✅ Some confectionary products generate strong revenue but lower profitability, suggesting increased operational costs."
)

# =========================================================
# RAW DATA
# =========================================================

st.markdown("---")

if st.checkbox("Show Raw Dataset"):

    st.dataframe(filtered_df)

