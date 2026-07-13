import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

st.title("🤖 Machine Learning")

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
# Find Classification Target Columns
# -----------------------------
classification_targets = []

for col in df.columns:

    # Object/String columns
    if df[col].dtype == "object":
        classification_targets.append(col)

    # Numeric columns with few unique values
    elif df[col].nunique() <= 20:
        classification_targets.append(col)

# If no classification target exists
if not classification_targets:
    st.error("No suitable classification target column found.")
    st.stop()

# -----------------------------
# Select Target Column
# -----------------------------
target = st.selectbox(
    "Select Target Column",
    classification_targets
)
# -----------------------------
# Model Selection
# -----------------------------
model_name = st.selectbox(
    "Select Model",
    [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest"
    ]
)

# -----------------------------
# Train Button
# -----------------------------
if st.button("🚀 Train Model"):

    data = df.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Fill missing values
    for col in data.columns:

        if pd.api.types.is_numeric_dtype(data[col]):
            data[col] = data[col].fillna(data[col].median())

        else:
            data[col] = data[col].fillna(data[col].mode()[0])

    # Encode categorical columns
    encoder = LabelEncoder()

    for col in data.select_dtypes(include=["object", "string", "category"]).columns:
        data[col] = encoder.fit_transform(data[col].astype(str))

    # Features & Target
    X = data.drop(columns=[target])
    y = data[target]

    # Check whether target is suitable for classification
    if y.nunique() > 20:
        st.error(
            "The selected target looks like a continuous variable. "
            "Please choose a categorical target for Classification."
        )
        st.stop()

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Select Model
    if model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)

    elif model_name == "Decision Tree":
        model = DecisionTreeClassifier(random_state=42)

    else:
        model = RandomForestClassifier(random_state=42)

    # Train
    model.fit(X_train, y_train)

    # Predict
    prediction = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, prediction)
    # Save values for Report page
    st.session_state["selected_model"] = model_name
    st.session_state["accuracy"] = round(accuracy * 100, 2)
    st.session_state["target"] = target

    # Display Results
    st.success("✅ Model Trained Successfully")

    st.write("### Model")
    st.write(model_name)

    st.write("### Accuracy")
    st.write(f"{accuracy * 100:.2f}%")