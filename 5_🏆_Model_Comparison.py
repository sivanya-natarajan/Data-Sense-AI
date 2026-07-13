import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

st.title("🏆 Model Comparison")

# -----------------------------
# Check Dataset
# -----------------------------
if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state.df.copy()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# Select Target Column
# -----------------------------
target = st.selectbox(
    "Select Target Column",
    df.columns
)

# -----------------------------
# Compare Models
# -----------------------------
if st.button("Compare Models"):

    data = df.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Fill Missing Values
    for col in data.columns:

        if pd.api.types.is_numeric_dtype(data[col]):
            data[col] = data[col].fillna(data[col].median())

        else:
            data[col] = data[col].fillna(data[col].mode()[0])

    # Encode Categorical Columns
    for col in data.select_dtypes(include=["object", "string", "category"]).columns:

        le = LabelEncoder()

        data[col] = le.fit_transform(data[col].astype(str))

    X = data.drop(columns=[target])
    y = data[target]

    # Check Classification Target
    if y.nunique() > 20:
        st.error("Selected target is not suitable for Classification.")
        st.stop()

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Models
    models = {

        "Logistic Regression":
        LogisticRegression(max_iter=1000),

        "Decision Tree":
        DecisionTreeClassifier(random_state=42),

        "Random Forest":
        RandomForestClassifier(random_state=42)

    }

    results = []

    best_accuracy = 0
    best_model = ""

    # Train All Models
    for name, model in models.items():

        model.fit(X_train, y_train)

        prediction = model.predict(X_test)

        accuracy = accuracy_score(y_test, prediction)

        results.append({

            "Model": name,
            "Accuracy (%)": round(accuracy * 100, 2)

        })

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_model = name

    result_df = pd.DataFrame(results)

    st.subheader("📊 Model Accuracy")

    st.dataframe(result_df, use_container_width=True)

    st.subheader("📈 Accuracy Comparison")

    st.bar_chart(
        result_df.set_index("Model")["Accuracy (%)"]
    )

    st.success(
        f"""
🏆 Best Model : {best_model}

Accuracy : {best_accuracy*100:.2f}%
"""
    )