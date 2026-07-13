import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------
# Page Title
# ----------------------------------------
st.title("🧹 Data Cleaning")

# ----------------------------------------
# Check Dataset
# ----------------------------------------
if "df" not in st.session_state:
    st.warning("⚠ Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# ----------------------------------------
# Dataset Overview
# ----------------------------------------
st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Rows", df.duplicated().sum())

st.divider()

# ----------------------------------------
# Dataset Quality Score
# ----------------------------------------
st.subheader("⭐ Dataset Quality Score")

total_cells = df.shape[0] * df.shape[1]
missing = df.isnull().sum().sum()

quality = ((total_cells - missing) / total_cells) * 100

st.progress(int(quality))
st.success(f"Quality Score : {quality:.2f}%")

st.divider()

# ----------------------------------------
# Missing Values Table
# ----------------------------------------
st.subheader("❗ Missing Values")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

st.dataframe(missing_df, use_container_width=True)

st.divider()

# ----------------------------------------
# Missing Values Chart
# ----------------------------------------
st.subheader("📊 Missing Values Chart")

missing_chart = df.isnull().sum()
missing_chart = missing_chart[missing_chart > 0]

if not missing_chart.empty:

    fig = px.bar(
        x=missing_chart.index,
        y=missing_chart.values,
        labels={
            "x": "Column",
            "y": "Missing Values"
        },
        title="Missing Values by Column"
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.success("🎉 No Missing Values Found!")

st.divider()

# ----------------------------------------
# Cleaning Options
# ----------------------------------------
st.subheader("🧹 Cleaning Options")

col1, col2 = st.columns(2)

# ----------------------------------------
# Remove Duplicates
# ----------------------------------------
with col1:

    if st.button("🗑 Remove Duplicate Rows"):

        before = df.shape[0]

        df = df.drop_duplicates()

        st.session_state["df"] = df

        after = df.shape[0]

        st.success(f"{before-after} Duplicate Rows Removed!")

        st.rerun()

# ----------------------------------------
# Fill Missing Values
# ----------------------------------------
with col2:

    if st.button("💊 Fill Missing Values"):

        for column in df.columns:

            # Categorical columns
            if df[column].dtype == "object":

                if not df[column].mode().empty:
                    df[column] = df[column].fillna(df[column].mode()[0])

            # Numeric columns
            else:

                if df[column].isnull().sum() > 0:

                    median = df[column].median()

                    if pd.notna(median):
                        df[column] = df[column].fillna(median)
                    else:
                        df[column] = df[column].fillna(0)

        st.session_state["df"] = df

        st.success("✅ Missing Values Filled Successfully!")

        st.rerun()

st.divider()

# ----------------------------------------
# Remove Missing Rows
# ----------------------------------------
if st.button("❌ Remove Rows With Missing Values"):

    before = df.shape[0]

    df = df.dropna()

    st.session_state["df"] = df

    after = df.shape[0]

    st.success(f"{before-after} Rows Removed Successfully!")

    st.rerun()

st.divider()

# ----------------------------------------
# Clean Dataset Preview
# ----------------------------------------
st.subheader("📋 Clean Dataset Preview")

st.dataframe(df.head(), use_container_width=True)

st.divider()

# ----------------------------------------
# Download Clean Dataset
# ----------------------------------------
csv = df.to_csv(index=False)

st.download_button(
    label="⬇ Download Clean Dataset",
    data=csv,
    file_name="Clean_Dataset.csv",
    mime="text/csv"
)