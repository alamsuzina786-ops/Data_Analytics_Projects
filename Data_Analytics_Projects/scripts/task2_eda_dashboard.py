import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Employee Data - EDA Dashboard")

file = st.file_uploader("Upload Cleaned Employee CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum())

    st.subheader("Basic Statistics")
    st.dataframe(df.describe())

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 1:

        st.subheader("Histogram")
        column = st.selectbox("Select Column", numeric_cols)

        fig, ax = plt.subplots()
        ax.hist(df[column].dropna())
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        st.subheader("Correlation Heatmap")

        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, ax=ax)
        st.pyplot(fig)

        st.subheader("Outlier Boxplot")

        fig, ax = plt.subplots()
        sns.boxplot(x=df[column], ax=ax)
        ax.set_xlabel(column)
        st.pyplot(fig)