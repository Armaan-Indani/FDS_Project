import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

st.title("Student Clustering using KMeans")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("app/data/student-mat.csv", sep=";")

df = load_data()

st.subheader("Raw Data")
st.dataframe(df.head())

# Preprocessing
df_clean = df[['age', 'Medu', 'Fedu', 'studytime', 'failures', 'absences',
               'G1', 'G2', 'G3', 'schoolsup', 'famsup', 'internet']].copy()

binary_map = {'yes': 1, 'no': 0}
df_clean['schoolsup'] = df_clean['schoolsup'].map(binary_map)
df_clean['famsup'] = df_clean['famsup'].map(binary_map)
df_clean['internet'] = df_clean['internet'].map(binary_map)

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean)

# Elbow Method
sse = []
K = range(1, 11)
for k in K:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    sse.append(km.inertia_)

st.subheader("Elbow Method")
fig, ax = plt.subplots()
ax.plot(K, sse, marker='o')
ax.set_xlabel('Number of clusters (k)')
ax.set_ylabel('Sum of Squared Errors (SSE)')
ax.set_title('Elbow Method For Optimal k')
st.pyplot(fig)

# Select k and fit model
k = st.slider("Select number of clusters (k)", min_value=2, max_value=10, value=3)
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels to dataframe
df_clean['Cluster'] = clusters

# PCA for 2D plotting
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

st.subheader("Clusters (PCA Projection)")
fig2, ax2 = plt.subplots()
scatter = ax2.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='Set2')
ax2.set_title("PCA-Reduced Clusters")
ax2.set_xlabel("PC1")
ax2.set_ylabel("PC2")
st.pyplot(fig2)

# Cluster centers
st.subheader("Cluster Summary")
st.dataframe(df_clean.groupby("Cluster").mean())
