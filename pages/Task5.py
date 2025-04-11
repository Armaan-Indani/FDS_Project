# pages/Task5.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Career Pathway Visualization", layout="wide")
st.title("🚀 Employee Success Stories & Career Pathways")

@st.cache_data
def load_data():
    file_path = os.path.join("app", "data", "4_Employee_HR-Employee-Attrition-dataset.csv")
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Basic preprocessing
df_clean = df.drop(columns=['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'])
df_clean['TotalWorkingYears'] = df_clean['TotalWorkingYears'].replace(0, df_clean['TotalWorkingYears'].median())
df_clean['EstimatedGraduationAge'] = df_clean['Age'] - df_clean['TotalWorkingYears']

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Career Timelines", "Education Path Mapping", "Income vs Education", "Department Insights"])

with tab1:
    selected_roles = st.multiselect(
        "Select Job Roles for Career Timeline",
        options=df_clean['JobRole'].unique(),
        default=['Research Scientist', 'Sales Executive']
    )

    st.subheader("📌 Career Timelines of Sample Employees")
    sample_employees = df_clean[df_clean['JobRole'].isin(selected_roles)].head(10)


    fig = go.Figure()
    for _, row in sample_employees.iterrows():
        fig.add_trace(go.Bar(
            x=[row['YearsAtCompany']],
            y=[f"{row['JobRole']} ({row['Age']} yrs)"],
            orientation='h',
            name=row['JobRole'],
            hovertext=f"Role: {row['JobRole']}<br>EducationField: {row['EducationField']}<br>TotalWorkingYears: {row['TotalWorkingYears']}"
        ))

    
    fig.update_layout(
        title="Career Timelines of Sample Employees",
        xaxis_title="Years at Company",
        yaxis_title="Employee (JobRole - Age)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("📚 Mapping Education Fields to Job Roles")
    edu_job_df = df_clean.groupby(['EducationField', 'JobRole']).size().reset_index(name='count')

    fig = px.sunburst(
        edu_job_df,
        path=['EducationField', 'JobRole'],
        values='count',
        title="Mapping Education Fields to Job Roles"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📊 Education Level vs Monthly Income")
    fig = px.scatter(
        df_clean,
        x='Education',
        y='MonthlyIncome',
        color='JobRole',
        size='TotalWorkingYears',
        hover_data=['EducationField'],
        title="How Education Level Impacts Monthly Income"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    selected_department = st.selectbox(
        "Select Department for Education vs Roles",
        options=df_clean['Department'].unique()
    )
    st.subheader(f"🏢 Job Roles vs Education Fields in {selected_department}")
    dept_df = df_clean[df_clean['Department'] == selected_department]

    fig = px.histogram(
        dept_df,
        x='JobRole',
        color='EducationField',
        title=f'Job Roles vs Education Fields in {selected_department} Department',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
