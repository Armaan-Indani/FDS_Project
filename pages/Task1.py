# pages/Task2.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

st.set_page_config(page_title="Course Explorer", layout="wide")
st.title("📚 Course Explorer and Recommendations")

# Load Data
@st.cache_data
def load_data():
    file_path = os.path.join("app", "data", "courses_preprocessed.csv")  # adjust if needed
    df = pd.read_csv(file_path)
    df['skills_list'] = df['skills_list'].apply(ast.literal_eval)
    return df

courses_df = load_data()

# Data Cleaning
courses_df['level'] = courses_df['level'].fillna('Unknown').str.strip()
courses_df = courses_df.dropna(subset=['rating'])
courses_df['reviewcount'] = courses_df['reviewcount'].apply(
    lambda x: int(float(x.replace('k', '')) * 1000) if isinstance(x, str) and 'k' in x else (
        int(x) if str(x).isdigit() else np.nan)
)
courses_df['rating'] = pd.to_numeric(courses_df['rating'], errors='coerce')
courses_df['duration'] = courses_df['duration'].str.replace(' Months', '').str.replace(' - ', '-')

# Sidebar Controls
st.sidebar.header("🔎 Filter Options")
goal_input = st.sidebar.text_input("Enter your skill goal (e.g., Data Analysis)", "")

# Main Sections
tab1, tab2, tab3 = st.tabs(["Overview", "Recommendations", "Visualizations"])

with tab1:
    st.subheader("Dataset Summary")
    st.dataframe(courses_df.head(10))
    st.write("Shape:", courses_df.shape)
    st.write("Missing Values:", courses_df.isnull().sum().sum())
    st.write("Unique Skills:", len(set(skill for sublist in courses_df['skills_list'].dropna() for skill in sublist)))

with tab2:
    st.subheader("Course Recommendations")

    if goal_input:
        st.markdown(f"### 🔍 Top Courses for Goal: `{goal_input}`")
        recommended = courses_df[courses_df['skills_list'].apply(
            lambda x: any(goal_input.lower() in skill.lower() or skill.lower() in goal_input.lower() for skill in x) if x else False)
        ]
        recommended = recommended.sort_values(by='rating', ascending=False).reset_index(drop=True)
        st.dataframe(recommended[['course', 'rating']].head(10))
    else:
        st.markdown("### 🎯 Top 10 Courses (Rating + Reviews)")
        top_courses = courses_df.sort_values(by=['rating', 'reviewcount'], ascending=[False, False]).reset_index(drop=True).head(10)
        st.dataframe(top_courses[['course', 'rating', 'reviewcount']])
        st.info("Enter a goal from the sidebar to see goal-based recommendations.")

with tab3:
    st.subheader("Top Skills by Course Frequency")
    skill_counts = courses_df['skills_list'].explode().value_counts().head(15)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=skill_counts.values, y=skill_counts.index, palette="viridis")
    plt.xlabel("Number of Courses")
    plt.ylabel("Skills")
    plt.title("Top 15 Skill Distribution")
    st.pyplot(plt.gcf())
    plt.clf()

    st.subheader("Top 20 Courses by Rating (min 50k reviews)")
    top_rating = courses_df[courses_df['reviewcount'] > 50000][['course', 'rating']].sort_values(by='rating', ascending=False).head(20)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='rating', y='course', data=top_rating, palette='Blues_r')
    plt.title("Top 20 Courses by Rating")
    st.pyplot(plt.gcf())
    plt.clf()

    # st.subheader("Heatmap: Top Courses by Rating & Popularity")
    # if 'popularity' not in courses_df.columns:
    #     courses_df['popularity'] = courses_df['rating'] * 100
    
    # top_heat = courses_df[['course', 'rating', 'popularity']].sort_values(by='rating', ascending=False).head(20)
    # pivot_table = top_heat.pivot_table(values='rating', index='course', columns='popularity', fill_value=0)

    # plt.figure(figsize=(14, 8))
    # sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=0.5)
    # plt.title("Heatmap of Top 20 Courses by Rating and Popularity")
    # st.pyplot(plt.gcf())
    # plt.clf()

    st.subheader("Skill Distribution of Goals")
    valid_levels = ['Beginner', 'Intermediate', 'Advanced']
    filtered_df = courses_df[courses_df['level'].isin(valid_levels)]
    
    plt.figure(figsize=(10, 6))
    sns.countplot(data=filtered_df, x='level', order=valid_levels, palette='viridis')
    plt.title("Skill Distribution of Goals")
    st.pyplot(plt.gcf())
    plt.clf()
