import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
import ast

# Set page config
st.set_page_config(page_title="In-Demand Skills Explorer", layout="wide")

st.title("🔍 In-Demand Skills vs Courses")

# Load datasets
courses_df = pd.read_csv("app/data/courses_preprocessed.csv")
jobs_df = pd.read_csv("app/data/jobs_preprocessed.csv")

# Fill missing values in 'skills'
courses_df['skills'] = courses_df['skills'].fillna('')
jobs_df['skills'] = jobs_df['skills'].fillna('')

courses_df['skills_list'] = courses_df['skills_list'].apply(ast.literal_eval)
jobs_df['skills_list'] = jobs_df['skills_list'].apply(ast.literal_eval)

# Count skill frequencies in jobs
all_job_skills = [skill for sublist in jobs_df['skills_list'] for skill in sublist]
skills_counter = Counter(all_job_skills)
skills_freq_df = pd.DataFrame(skills_counter.items(), columns=['skill', 'count']).sort_values(by='count', ascending=False)

# Top N skill slider
top_n = st.slider("Select number of top in-demand skills to view:", 5, 30, 10)
top_skills = skills_freq_df.head(top_n)

# Plot top skills
st.subheader("📊 Top In-Demand Skills from Job Postings")
fig, ax = plt.subplots()
ax.bar(top_skills['skill'], top_skills['count'])
plt.xticks(rotation=45)
plt.xlabel("Skills")
plt.ylabel("Frequency")
plt.title("Top In-Demand Skills")
st.pyplot(fig)


# Use all job skill frequencies for scoring (not just top N)
all_job_skills = [skill for skills_row in jobs_df['skills_list'] for skill in skills_row]
all_skill_counts = Counter(all_job_skills)

# Create full skill_weights dict from all job data
skill_weights = dict(all_skill_counts)
all_demand_skills = set(skill_weights.keys())

# Weighted score based on all skill frequencies
def weighted_skill_score(skills):
    return sum(skill_weights.get(skill, 0) for skill in skills)

# Filter out only those skills which are in demand
def filter_in_demand_skills(skills):
    return [skill for skill in skills if skill in all_demand_skills]

courses_df['in_demand_skill_score'] = courses_df['skills_list'].apply(weighted_skill_score)
courses_df['filtered_skills'] = courses_df['skills_list'].apply(filter_in_demand_skills)

# Filter to only meaningful courses
top_courses = courses_df[courses_df['in_demand_skill_score'] > 0]
top_courses = top_courses.sort_values(by='in_demand_skill_score', ascending=False)


st.subheader("📚 Courses Matching In-Demand Skills - Sorted in order of skill score")
st.dataframe(top_courses[['partner', 'course', 'rating', 'level','certificatetype','duration','crediteligibility','filtered_skills', 'in_demand_skill_score']].reset_index(drop=True))


st.header("📊 Filter Courses")

# Skills filter
selected_skills = st.multiselect("Skills:", options=sorted(all_demand_skills), default=[])

# Partner filter
partners = sorted(top_courses['partner'].dropna().unique())
selected_partners = st.multiselect("Partner", partners, default=[])

# Level filter
levels = sorted(top_courses['level'].dropna().unique())
selected_levels = st.multiselect("Level", levels, default=[])

# Certificate Type filter
cert_types = sorted(top_courses['certificatetype'].dropna().unique())
selected_cert_types = st.multiselect("Certificate Type", cert_types, default=[])

# Credit Eligibility filter
credit_options = sorted(top_courses['crediteligibility'].dropna().unique())
selected_credits = st.multiselect("Credit Eligibility", credit_options, default=[])

# Rating filter
min_rating, max_rating = st.slider(
    "Rating Range", 
    float(top_courses['rating'].min()), 
    float(top_courses['rating'].max()), 
    (float(top_courses['rating'].min()), float(top_courses['rating'].max()))
)

# If user leaves any multiselect empty, assume "all"
if not selected_partners:
    selected_partners = partners

if not selected_levels:
    selected_levels = levels

if not selected_cert_types:
    selected_cert_types = cert_types

if not selected_credits:
    selected_credits = credit_options


# Apply user-selected skill filter
if selected_skills:
    top_courses = top_courses[top_courses['filtered_skills'].apply(
        lambda skills: any(skill in skills for skill in selected_skills)
    )]

filtered_courses = top_courses[
    (top_courses['partner'].isin(selected_partners)) &
    (top_courses['level'].isin(selected_levels)) &
    (top_courses['certificatetype'].isin(selected_cert_types)) &
    (top_courses['crediteligibility'].isin(selected_credits)) &
    (top_courses['rating'] >= min_rating) &
    (top_courses['rating'] <= max_rating)
]

#     (top_courses['duration'] >= min_duration) &
#     (top_courses['duration'] <= max_duration)

# Display results
st.subheader("📚 Courses Matching In-Demand Skills")
st.dataframe(filtered_courses[['partner', 'course', 'rating', 'level','certificatetype','duration','crediteligibility','filtered_skills', 'in_demand_skill_score']].reset_index(drop=True))
