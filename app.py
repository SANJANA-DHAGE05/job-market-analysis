import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="USA IT Job Market Analysis 2025",
    page_icon="🇺🇸",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/jobs_cleaned.csv')
    
    # Map state abbreviations to full names
    state_mapping = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'Washington DC'
    }
    
    # Replace abbreviations with full names
    df['state'] = df['state'].map(state_mapping).fillna(df['state'])
    
    return df

df = load_data()

# Title
st.title("🇺🇸 USA IT Job Market Analysis 2025")
st.markdown("""
Comprehensive analysis of **2,200+ data analyst and data scientist jobs** in the United States from Glassdoor, revealing:
- 💰 Salary trends across seniority levels and locations
- 🛠️ Most in-demand technical skills
- 📍 Top hiring states and cities
- 🏢 Leading companies hiring data professionals
""")

st.divider()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Seniority filter
seniority_options = ['All'] + sorted(df['seniority'].unique().tolist())
selected_seniority = st.sidebar.selectbox("Seniority Level", seniority_options)

# State filter
state_options = ['All'] + sorted(df['state'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("State (USA)", state_options)

# Salary filter
min_sal, max_sal = int(df['avg_salary_k'].min()), int(df['avg_salary_k'].max())
salary_range = st.sidebar.slider("Salary Range ($K)", min_sal, max_sal, (min_sal, max_sal))

# Apply filters
filtered_df = df[df['avg_salary_k'].between(salary_range[0], salary_range[1])]

if selected_seniority != 'All':
    filtered_df = filtered_df[filtered_df['seniority'] == selected_seniority]

if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['state'] == selected_state]

st.sidebar.metric("Jobs Matching Filters", len(filtered_df))

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs", len(filtered_df))

with col2:
    median_salary = filtered_df['avg_salary_k'].median()
    st.metric("Median Salary", f"${median_salary:.0f}K")

with col3:
    unique_companies = filtered_df['company'].nunique()
    st.metric("Unique Companies", unique_companies)

with col4:
    states_count = filtered_df['state'].nunique()
    st.metric("States", states_count)

st.divider()

# Row 1: Salary Analysis
st.header("💰 Salary Analysis")

col1, col2 = st.columns(2)

with col1:
    # Salary distribution
    fig_salary = px.histogram(
        filtered_df,
        x='avg_salary_k',
        nbins=30,
        title='Salary Distribution',
        labels={'avg_salary_k': 'Salary ($K)'},
        color_discrete_sequence=['#636EFA']
    )
    fig_salary.add_vline(x=median_salary, line_dash="dash", line_color="red",
                         annotation_text=f"Median: ${median_salary:.0f}K")
    fig_salary.update_layout(
        xaxis_title="Annual Salary ($K USD)",
        yaxis_title="Number of Jobs",
        showlegend=False
    )
    st.plotly_chart(fig_salary, use_container_width=True)

with col2:
    # Salary by seniority
    salary_by_seniority = filtered_df.groupby('seniority')['avg_salary_k'].median().reset_index()
    salary_by_seniority = salary_by_seniority.sort_values('avg_salary_k')
    
    fig_seniority = px.bar(
        salary_by_seniority,
        x='avg_salary_k',
        y='seniority',
        orientation='h',
        title='Median Salary by Seniority Level',
        labels={'avg_salary_k': 'Median Salary ($K)', 'seniority': 'Seniority Level'},
        color='avg_salary_k',
        color_continuous_scale='Viridis',
        text='avg_salary_k'
    )
    fig_seniority.update_traces(texttemplate='$%{text:.0f}K', textposition='outside')
    fig_seniority.update_layout(showlegend=False)
    st.plotly_chart(fig_seniority, use_container_width=True)

# Salary by state
state_salary = filtered_df.groupby('state').agg({
    'avg_salary_k': 'median',
    'Job Title': 'count'
}).rename(columns={'Job Title': 'count'}).reset_index()
state_salary = state_salary[state_salary['count'] >= 10].sort_values('avg_salary_k', ascending=False).head(15)

fig_state_sal = px.bar(
    state_salary,
    x='avg_salary_k',
    y='state',
    orientation='h',
    title='Median Salary by Top 15 States (minimum 10 jobs)',
    labels={'avg_salary_k': 'Median Salary ($K)', 'state': 'State'},
    color='avg_salary_k',
    color_continuous_scale='RdYlGn',
    text='avg_salary_k'
)
fig_state_sal.update_traces(texttemplate='$%{text:.0f}K', textposition='outside')
fig_state_sal.update_layout(showlegend=False, height=500)
st.plotly_chart(fig_state_sal, use_container_width=True)

st.divider()

# Row 2: Skills Analysis
st.header("🛠️ Top Skills Analysis")

skill_cols = [col for col in filtered_df.columns if col.startswith('skill_')]
skill_counts = {}
for col in skill_cols:
    skill_name = col.replace('skill_', '').replace('_', ' ').title()
    count = filtered_df[col].sum()
    if count > 0:
        skill_counts[skill_name] = count

top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15])

skills_df = pd.DataFrame({
    'Skill': list(top_skills.keys()),
    'Count': list(top_skills.values())
})
skills_df['Percentage'] = (skills_df['Count'] / len(filtered_df) * 100).round(1)

col1, col2 = st.columns([2, 1])

with col1:
    fig_skills = px.bar(
        skills_df,
        x='Count',
        y='Skill',
        orientation='h',
        title='Top 15 Most In-Demand Skills',
        labels={'Count': 'Number of Jobs'},
        color='Count',
        color_continuous_scale='Blues',
        text='Count'
    )
    fig_skills.update_traces(textposition='outside')
    fig_skills.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_skills, use_container_width=True)

with col2:
    st.subheader("Skills Demand")
    st.dataframe(
        skills_df[['Skill', 'Percentage']].rename(columns={'Percentage': '% of Jobs'}),
        hide_index=True,
        height=500
    )

st.divider()

# Row 3: Geographic Distribution
st.header("📍 Geographic Distribution (USA)")

col1, col2 = st.columns(2)

with col1:
    # Top states
    top_states = filtered_df['state'].value_counts().head(10).reset_index()
    top_states.columns = ['State', 'Jobs']
    
    fig_states = px.bar(
        top_states,
        x='Jobs',
        y='State',
        orientation='h',
        title='Top 10 States by Job Count',
        color='Jobs',
        color_continuous_scale='Greens',
        text='Jobs'
    )
    fig_states.update_traces(textposition='outside')
    fig_states.update_layout(showlegend=False)
    st.plotly_chart(fig_states, use_container_width=True)

with col2:
    # Top cities
    top_cities = filtered_df['city'].value_counts().head(10).reset_index()
    top_cities.columns = ['City', 'Jobs']
    
    fig_cities = px.bar(
        top_cities,
        x='Jobs',
        y='City',
        orientation='h',
        title='Top 10 Cities by Job Count',
        color='Jobs',
        color_continuous_scale='Oranges',
        text='Jobs'
    )
    fig_cities.update_traces(textposition='outside')
    fig_cities.update_layout(showlegend=False)
    st.plotly_chart(fig_cities, use_container_width=True)

st.divider()

# Row 4: Companies and Industries
st.header("🏢 Top Hiring Companies & Industries")

col1, col2 = st.columns(2)

with col1:
    top_companies = filtered_df['company'].value_counts().head(15).reset_index()
    top_companies.columns = ['Company', 'Jobs']
    
    fig_companies = px.bar(
        top_companies,
        x='Jobs',
        y='Company',
        orientation='h',
        title='Top 15 Hiring Companies',
        color='Jobs',
        color_continuous_scale='Purples',
        text='Jobs'
    )
    fig_companies.update_traces(textposition='outside')
    fig_companies.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_companies, use_container_width=True)

with col2:
    top_industries = filtered_df['Industry'].value_counts().head(10).reset_index()
    top_industries.columns = ['Industry', 'Jobs']
    
    fig_industries = px.pie(
        top_industries,
        values='Jobs',
        names='Industry',
        title='Top 10 Industries Hiring',
        hole=0.4
    )
    fig_industries.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_industries, use_container_width=True)

st.divider()

# Key Insights
st.header("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 Salary by Level")
    for level in ['Junior', 'Mid-Level', 'Senior']:
        level_data = filtered_df[filtered_df['seniority'] == level]['avg_salary_k']
        if len(level_data) > 0:
            st.metric(level, f"${level_data.median():.0f}K", f"{len(level_data)} jobs")

with col2:
    st.subheader("🛠️ Must-Have Skills")
    top_3 = list(top_skills.keys())[:3]
    for i, skill in enumerate(top_3, 1):
        pct = (top_skills[skill] / len(filtered_df)) * 100
        st.write(f"**{i}. {skill}** - {pct:.0f}% of jobs")

with col3:
    st.subheader("📍 Top Location")
    if not filtered_df.empty:
        top_state = filtered_df['state'].mode()[0]
        top_state_jobs = len(filtered_df[filtered_df['state'] == top_state])
        top_state_salary = filtered_df[filtered_df['state'] == top_state]['avg_salary_k'].median()
        
        st.metric(top_state, f"{top_state_jobs} jobs")
        st.write(f"**Median Salary:** ${top_state_salary:.0f}K")

# Additional Insights Section
st.divider()
st.header("📊 Additional Market Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Salary Growth Potential")
    junior_sal = filtered_df[filtered_df['seniority'] == 'Junior']['avg_salary_k'].median()
    senior_sal = filtered_df[filtered_df['seniority'] == 'Senior']['avg_salary_k'].median()
    
    if pd.notna(junior_sal) and pd.notna(senior_sal) and junior_sal > 0:
        growth_pct = ((senior_sal - junior_sal) / junior_sal) * 100
        st.metric("Junior → Senior Growth", f"+{growth_pct:.0f}%", f"${senior_sal - junior_sal:.0f}K increase")
    
    st.write(f"""
    **Career Progression:**
    - Junior roles start at ~${junior_sal:.0f}K
    - Senior roles reach ~${senior_sal:.0f}K
    - Strong growth potential in data careers
    """)

with col2:
    st.subheader("Market Concentration")
    top_3_states = filtered_df['state'].value_counts().head(3)
    top_3_pct = (top_3_states.sum() / len(filtered_df)) * 100
    
    st.metric("Top 3 States", f"{top_3_pct:.0f}%", "of all jobs")
    
    st.write("**Geographic Concentration:**")
    for state, count in top_3_states.items():
        pct = (count / len(filtered_df)) * 100
        st.write(f"• {state}: {pct:.1f}% ({count} jobs)")

# Footer
st.divider()
st.markdown("""
---
### 📊 About This Analysis

**Data Source:** Glassdoor USA (2,253 data analyst & data scientist job postings)  
**Analysis Period:** 2024-2025  
**Geographic Coverage:** All 50 US states + DC  
**Skills Analyzed:** 25+ technical skills extracted from job descriptions

**Methodology:**
- Data collected from Glassdoor job postings
- Salary ranges extracted and averaged
- Skills identified through keyword matching in job descriptions
- Seniority levels classified from job titles
- Duplicates removed to ensure accuracy

---



*This dashboard helps job seekers understand the data job market. Use filters to explore salaries, skills, and opportunities based on your preferences.*

⭐ **Found this helpful? Star the project on GitHub!**
""")