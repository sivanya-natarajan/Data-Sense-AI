import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page Title
# ---------------------------------------

st.title("📊 Exploratory Data Analysis (EDA)")

# ---------------------------------------
# Check Dataset
# ---------------------------------------

if "df" not in st.session_state:

    st.warning("⚠ Please upload a dataset first.")

    st.stop()

df = st.session_state["df"]

# ---------------------------------------
# Dataset Information
# ---------------------------------------

st.subheader("📋 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])

col2.metric("Columns", df.shape[1])

col3.metric("Missing Values", df.isnull().sum().sum())

st.divider()

# ---------------------------------------
# Numeric Columns
# ---------------------------------------

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if len(numeric_columns) == 0:

    st.error("No Numeric Columns Found")

    st.stop()

# ---------------------------------------
# Histogram
# ---------------------------------------

st.subheader("📉 Histogram")

hist_column = st.selectbox(
    "Select Column",
    numeric_columns
)

fig = px.histogram(
    df,
    x=hist_column,
    nbins=30,
    title=f"Distribution of {hist_column}"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------
# Box Plot
# ---------------------------------------

st.subheader("📦 Box Plot")

fig = px.box(
    df,
    y=hist_column,
    title=f"Box Plot of {hist_column}"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------
# Scatter Plot
# ---------------------------------------

st.subheader("📈 Scatter Plot")

x_axis = st.selectbox(
    "Select X-axis",
    numeric_columns,
    key="x"
)

y_axis = st.selectbox(
    "Select Y-axis",
    numeric_columns,
    index=1,
    key="y"
)

fig = px.scatter(
    df,
    x=x_axis,
    y=y_axis,
    title=f"{x_axis} vs {y_axis}"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------
# Correlation Heatmap
# ---------------------------------------

st.subheader("🔥 Correlation Heatmap")

corr = df[numeric_columns].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------
# Bar Chart
# ---------------------------------------

st.subheader("📊 Bar Chart")

bar_column = st.selectbox(
    "Select Column for Bar Chart",
    numeric_columns,
    key="bar"
)

value_counts = df[bar_column].value_counts().head(10)

fig = px.bar(
    x=value_counts.index.astype(str),
    y=value_counts.values,
    labels={
        "x":"Value",
        "y":"Count"
    },
    title=f"Top Values of {bar_column}"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------
# Pie Chart
# ---------------------------------------

st.subheader("🥧 Pie Chart")

cat_columns = df.select_dtypes(include="object").columns.tolist()

if len(cat_columns) > 0:

    pie_column = st.selectbox(
        "Select Categorical Column",
        cat_columns
    )

    pie_data = df[pie_column].value_counts().head(10)

    fig = px.pie(
        names=pie_data.index,
        values=pie_data.values,
        title=f"{pie_column} Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.info("No categorical columns available.")

st.divider()

# ---------------------------------------
# Statistical Summary
# ---------------------------------------

st.subheader("📑 Statistical Summary")

st.dataframe(df.describe(), use_container_width=True)