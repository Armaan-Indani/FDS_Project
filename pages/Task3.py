import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

st.title("Student Clustering and Recommendation System")

@st.cache_data
def load_data():
    return pd.read_csv("app/data/student-mat.csv", sep=';')

df = load_data()
st.subheader("Raw Dataset Preview")
st.dataframe(df.head())

# Step 2: Preprocessing
df_clean = df[['age', 'Medu', 'Fedu', 'studytime', 'failures', 'absences',
               'G1', 'G2', 'G3', 'schoolsup', 'famsup', 'internet']].copy()

binary_map = {'yes': 1, 'no': 0}
df_clean['schoolsup'] = df_clean['schoolsup'].map(binary_map)
df_clean['famsup'] = df_clean['famsup'].map(binary_map)
df_clean['internet'] = df_clean['internet'].map(binary_map)

# Step 3: Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean)

# Step 4: Elbow Method
sse = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    sse.append(km.inertia_)

st.subheader("Elbow Method for Optimal k")
fig1, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(range(1, 11), sse, marker='o')
ax1.set_xlabel("Number of Clusters")
ax1.set_ylabel("SSE (Inertia)")
ax1.grid(True)
st.pyplot(fig1)

# Step 5: Clustering
k = st.slider("Select number of clusters", 2, 10, 4)
kmeans = KMeans(n_clusters=k, random_state=42)
df_clean['Cluster'] = kmeans.fit_predict(X_scaled)

# Step 6: PCA
pca = PCA(n_components=2)
reduced = pca.fit_transform(X_scaled)
df_clean['PCA1'] = reduced[:, 0]
df_clean['PCA2'] = reduced[:, 1]

st.subheader("PCA Cluster Visualization")
fig2, ax2 = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=df_clean, x='PCA1', y='PCA2', hue='Cluster', palette='tab10', ax=ax2)
st.pyplot(fig2)

# Step 7: Silhouette Score
score = silhouette_score(X_scaled, df_clean['Cluster'])
st.write("Silhouette Score:", round(score, 4))

# Step 8: Cluster Academic Summary
cluster_summary = df_clean.groupby('Cluster')[['G1', 'G2', 'G3', 'studytime', 'failures']].mean()
st.subheader("Cluster Academic Summary")
st.dataframe(cluster_summary)

# Step 9: Recommendations
st.subheader("Recommendations per Cluster")
for cluster_id, row in cluster_summary.iterrows():
    if row['G3'] < 10:
        st.write(f"Cluster {cluster_id}: Recommend academic support or tutoring.")
    else:
        st.write(f"Cluster {cluster_id}: Recommend enrichment or advanced coursework.")

# Step 10: Visualizations
st.subheader("Grade Distribution per Cluster")
fig3, ax3 = plt.subplots(figsize=(7, 4))
sns.boxplot(x='Cluster', y='G3', data=df_clean, ax=ax3)
st.pyplot(fig3)

st.subheader("Student Count per Cluster")
fig4, ax4 = plt.subplots(figsize=(6, 4))
sns.countplot(x='Cluster', data=df_clean, ax=ax4)
st.pyplot(fig4)

st.subheader("Cluster-wise Feature Heatmap")
cluster_features = df_clean.groupby('Cluster')[df_clean.columns[:-4]].mean()
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.heatmap(cluster_features, annot=True, cmap="YlGnBu", ax=ax5)
st.pyplot(fig5)

st.subheader("Feature Correlation Matrix")
fig6, ax6 = plt.subplots(figsize=(10, 7))
sns.heatmap(df_clean.corr(), cmap='coolwarm', annot=True, ax=ax6)
st.pyplot(fig6)

# Optional Labels
df_clean['Cluster_Label'] = df_clean['Cluster'].map({
    0: 'High Achiever',
    1: 'Needs Attention',
    2: 'Moderate Performer',
    3: 'Irregular Attendance'
})

st.subheader("Cluster Label Distribution")
fig7, ax7 = plt.subplots(figsize=(6, 4))
sns.countplot(data=df_clean, x='Cluster_Label', ax=ax7)
plt.xticks(rotation=45)
st.pyplot(fig7)
