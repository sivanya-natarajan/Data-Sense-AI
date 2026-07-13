import streamlit as st
import base64

# Page Configuration
st.set_page_config(
    page_title="DataSense AI",
    page_icon="📊",
    layout="wide"
)

# Function to set background image
def add_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background:
                linear-gradient(rgba(255,255,255,0.60), rgba(255,255,255,0.60)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        h1, h2, h3, h4, h5, h6, p, li {{
            color: black !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

# Add background image
add_bg("images/BG.png")

# Header
st.markdown(
    """
    <h1 style="text-align:center;">📊 DataSense AI</h1>
    <h3 style="text-align:center;">Intelligent Data Analytics Platform</h3>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# Main Content
st.markdown("""
# Welcome

DataSense AI is a no-code data analytics platform built using **Python**, **Streamlit**, and **Machine Learning**.

## 🚀 Features

- 📁 Upload CSV Dataset
- 🧹 Data Cleaning
- 📊 Exploratory Data Analysis (EDA)
- 🤖 Machine Learning Models
- 🏆 Model Comparison
- 📄 Download Reports

---

## 📌 How to Use

1. Open **Upload** from the left sidebar.
2. Upload any CSV dataset.
3. Clean the data.
4. Explore visualizations.
5. Train ML models.
6. Download your results.
""")