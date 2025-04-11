# pages/Task4.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="📊 Student Performance Clustering", layout="wide")
st.title("📈 Student Struggles and Adaptive Learning Insights")

@st.cache_data
def load_data():
    df = pd.read_csv("app/data/StudentsPerformance.csv")
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df

df = load_data()

# Add calculated fields
score_columns = ['math_score', 'reading_score', 'writing_score']

def identify_struggles(row):
    struggles = []
    if row['math_score'] < 60: struggles.append('Math')
    if row['reading_score'] < 60: struggles.append('Reading')
    if row['writing_score'] < 60: struggles.append('Writing')
    return struggles

def recommend_resources(subjects):
    resources = []
    for subject in subjects:
        if subject == 'Math':
            resources.append("Khan Academy - Math Basics")
        elif subject == 'Reading':
            resources.append("Coursera - Reading Comprehension")
        elif subject == 'Writing':
            resources.append("edX - Academic Writing Essentials")
    return resources if resources else ["Advanced Learning Track"]

df['struggling_subjects'] = df.apply(identify_struggles, axis=1)
df['struggle_count'] = df['struggling_subjects'].apply(len)
df['recommended_resources'] = df['struggling_subjects'].apply(recommend_resources)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Visual Insights", "Clustering", "Recommendations"])

with tab1:
    st.subheader("📌 Dataset Snapshot")
    st.dataframe(df.head(10))
    st.write("Shape:", df.shape)
    st.write("Missing Values:", df.isnull().sum().sum())

    st.markdown("### 📊 Summary Statistics")
    st.dataframe(df.describe())

with tab2:
    st.subheader("📉 Score Distributions")
    for col in score_columns:
        st.markdown(f"**{col.replace('_', ' ').title()}**")
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f'{col.capitalize()} Distribution')
        st.pyplot(fig)

    st.markdown("### 🚨 Subjects Where Students Struggle")
    all_struggles = df['struggling_subjects'].explode().dropna()
    struggle_df = pd.DataFrame({'subject': all_struggles})
    fig, ax = plt.subplots()
    sns.countplot(data=struggle_df, x='subject', ax=ax)
    ax.set_title("Subjects Where Students Struggle Most")
    st.pyplot(fig)

    st.markdown("### 📦 Struggle Count by Gender")
    fig, ax = plt.subplots()
    sns.boxplot(x='gender', y='struggle_count', data=df, ax=ax)
    ax.set_title("Struggle Count by Gender")
    st.pyplot(fig)

with tab3:
    st.subheader("🧠 Clustering Students Based on Scores")

    X = df[score_columns]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    st.markdown("### 📊 Score Cluster Overview")
    fig = sns.pairplot(df, hue="cluster", vars=score_columns)
    st.pyplot(fig)

    st.markdown("### 🔍 PCA Visualization of Clusters")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df['pca1'] = X_pca[:, 0]
    df['pca2'] = X_pca[:, 1]
    fig, ax = plt.subplots()
    sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=df, hue='course', palette="Set2", legend=False, ax=ax)
    ax.set_title("PCA of Student Clusters")
    st.pyplot(fig)

with tab4:
    st.subheader("📚 Learning Recommendations")

    st.markdown("### 📈 Average Scores by Struggle Count")
    avg_by_struggle = df.groupby("struggle_count")[score_columns].mean().round(1)
    st.dataframe(avg_by_struggle)

    st.markdown("### 🧾 Sample Recommendations")
    st.dataframe(df[["math_score", "reading_score", "writing_score", 
                     "struggling_subjects", "recommended_resources", "cluster"]].head(10))

