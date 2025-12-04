import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="USA vs India IT Job Market 2025",
    page_icon="🌍",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    # Load USA data
    df_usa = pd.read_csv('data/processed/usa_jobs_cleaned.csv')
    
    # Load India data
    df_india = pd.read_csv('data/processed/india_jobs_cleaned.csv')
    
    # Combine (we'll filter by country later)
    # Note: USA has avg_salary_usd, India has avg_salary_lpa
    return df_usa, df_india

df_usa, df_india = load_data()

# Title
st.title("🌍 USA vs India IT Job Market Analysis 2025")
st.markdown("""
**Comprehensive comparison** of IT job markets across USA and India:
- 💰 Salary comparisons (adjusted for PPP)
- 🛠️ Skill demand differences
- 📊 Job role distribution
- 📍 Top hiring locations
""")

st.divider()

# ===== SIDEBAR FILTERS =====
st.sidebar.header("🔍 Filters")

# Country selector
country_option = st.sidebar.radio(
    "Select View",
    ["USA Only", "India Only", "Compare Both"]
)

# Job Category Filter
all_categories_usa = df_usa['job_category'].unique().tolist()
all_categories_india = df_india['job_category'].unique().tolist()
all_categories = sorted(list(set(all_categories_usa + all_categories_india)))

selected_category = st.sidebar.multiselect(
    "Job Categories",
    all_categories,
    default=all_categories[:3]  # Select first 3 by default
)

# Seniority filter
seniority_option = st.sidebar.selectbox(
    "Seniority Level",
    ["All", "Junior", "Mid-Level", "Senior"]
)

# Apply filters
def filter_data(df, categories, seniority):
    filtered = df[df['job_category'].isin(categories)]
    if seniority != "All":
        filtered = filtered[filtered['seniority'] == seniority]
    return filtered

df_usa_filtered = filter_data(df_usa, selected_category, seniority_option)
df_india_filtered = filter_data(df_india, selected_category, seniority_option)

# Display counts
st.sidebar.metric("USA Jobs", len(df_usa_filtered))
st.sidebar.metric("India Jobs", len(df_india_filtered))

# ===== MAIN METRICS =====
if country_option == "USA Only":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total USA Jobs", len(df_usa_filtered))
    with col2:
        median_sal = df_usa_filtered['avg_salary_usd'].median()
        st.metric("Median Salary (USA)", f"${median_sal:.0f}K")
    with col3:
        st.metric("Companies", df_usa_filtered['company'].nunique())
    with col4:
        st.metric("Locations", df_usa_filtered['location'].nunique())

elif country_option == "India Only":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total India Jobs", len(df_india_filtered))
    with col2:
        median_sal = df_india_filtered['avg_salary_lpa'].median()
        st.metric("Median Salary (India)", f"₹{median_sal:.1f} LPA")
    with col3:
        st.metric("Companies", df_india_filtered['company'].nunique())
    with col4:
        st.metric("Locations", df_india_filtered['location'].nunique())

else:  # Compare Both
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("USA Jobs", len(df_usa_filtered))
        st.metric("India Jobs", len(df_india_filtered))
    
    with col2:
        usa_sal = df_usa_filtered['avg_salary_usd'].median()
        india_sal = df_india_filtered['avg_salary_lpa'].median()
        st.metric("USA Salary", f"${usa_sal:.0f}K")
        st.metric("India Salary", f"₹{india_sal:.1f}L")
    
    with col3:
        # Convert India LPA to USD (rough: 1 LPA = $1.2K)
        india_sal_usd = india_sal * 1.2
        ratio = usa_sal / india_sal_usd if india_sal_usd > 0 else 0
        st.metric("USA/India Salary Ratio", f"{ratio:.1f}x")
        st.caption("(Absolute terms)")
    
    with col4:
        # PPP adjusted (rough: divide by 3)
        ppp_ratio = ratio / 3 if ratio > 0 else 0
        st.metric("PPP Adjusted Ratio", f"{ppp_ratio:.1f}x")
        st.caption("(Real purchasing power)")

st.divider()

# ===== SALARY COMPARISON =====
st.header("💰 Salary Analysis")

if country_option == "Compare Both":
    col1, col2 = st.columns(2)
    
    with col1:
        # USA Salary Distribution
        fig_usa = px.histogram(
            df_usa_filtered,
            x='avg_salary_usd',
            nbins=30,
            title='USA Salary Distribution ($K)',
            labels={'avg_salary_usd': 'Salary ($K USD)'},
            color_discrete_sequence=['#1f77b4']
        )
        median_usa = df_usa_filtered['avg_salary_usd'].median()
        fig_usa.add_vline(x=median_usa, line_dash="dash", line_color="red",
                         annotation_text=f"Median: ${median_usa:.0f}K")
        st.plotly_chart(fig_usa, use_container_width=True)
    
    with col2:
        # India Salary Distribution
        fig_india = px.histogram(
            df_india_filtered,
            x='avg_salary_lpa',
            nbins=30,
            title='India Salary Distribution (LPA)',
            labels={'avg_salary_lpa': 'Salary (₹ LPA)'},
            color_discrete_sequence=['#ff7f0e']
        )
        median_india = df_india_filtered['avg_salary_lpa'].median()
        fig_india.add_vline(x=median_india, line_dash="dash", line_color="red",
                           annotation_text=f"Median: ₹{median_india:.1f}L")
        st.plotly_chart(fig_india, use_container_width=True)
    
    # Salary by Category - Comparison
    st.subheader("Salary by Job Category")
    
    usa_by_cat = df_usa_filtered.groupby('job_category')['avg_salary_usd'].median().reset_index()
    india_by_cat = df_india_filtered.groupby('job_category')['avg_salary_lpa'].median().reset_index()
    
    # Convert India to USD for comparison
    india_by_cat['avg_salary_usd_equiv'] = india_by_cat['avg_salary_lpa'] * 1.2
    
    comparison_data = pd.merge(
        usa_by_cat, india_by_cat[['job_category', 'avg_salary_usd_equiv']], 
        on='job_category', how='outer'
    ).fillna(0)
    
    fig_comparison = go.Figure()
    fig_comparison.add_trace(go.Bar(
        name='USA',
        x=comparison_data['job_category'],
        y=comparison_data['avg_salary_usd'],
        marker_color='#1f77b4'
    ))
    fig_comparison.add_trace(go.Bar(
        name='India (USD equivalent)',
        x=comparison_data['job_category'],
        y=comparison_data['avg_salary_usd_equiv'],
        marker_color='#ff7f0e'
    ))
    
    fig_comparison.update_layout(
        title='Median Salary Comparison by Role (USD)',
        xaxis_title='Job Category',
        yaxis_title='Salary ($K USD)',
        barmode='group',
        height=500
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

elif country_option == "USA Only":
    col1, col2 = st.columns(2)
    
    with col1:
        fig_usa = px.histogram(
            df_usa_filtered,
            x='avg_salary_usd',
            nbins=30,
            title='USA Salary Distribution',
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig_usa, use_container_width=True)
    
    with col2:
        usa_by_cat = df_usa_filtered.groupby('job_category')['avg_salary_usd'].median().sort_values(ascending=False).reset_index()
        fig_cat = px.bar(
            usa_by_cat,
            x='avg_salary_usd',
            y='job_category',
            orientation='h',
            title='Median Salary by Category',
            color='avg_salary_usd',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_cat, use_container_width=True)

else:  # India Only
    col1, col2 = st.columns(2)
    
    with col1:
        fig_india = px.histogram(
            df_india_filtered,
            x='avg_salary_lpa',
            nbins=30,
            title='India Salary Distribution',
            color_discrete_sequence=['#ff7f0e']
        )
        st.plotly_chart(fig_india, use_container_width=True)
    
    with col2:
        india_by_cat = df_india_filtered.groupby('job_category')['avg_salary_lpa'].median().sort_values(ascending=False).reset_index()
        fig_cat = px.bar(
            india_by_cat,
            x='avg_salary_lpa',
            y='job_category',
            orientation='h',
            title='Median Salary by Category (LPA)',
            color='avg_salary_lpa',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# ===== SKILLS COMPARISON =====
st.header("🛠️ Skills Comparison")

# Get skill columns that exist in both datasets
skill_cols_usa = [col for col in df_usa.columns if col.startswith('skill_')]
skill_cols_india = [col for col in df_india.columns if col.startswith('skill_')]

# Find common skills
common_skill_cols = list(set(skill_cols_usa) & set(skill_cols_india))

if len(common_skill_cols) == 0:
    st.warning("⚠️ Skills data not available for comparison. Skills were extracted from USA data but may not be present in India data.")
    st.info("The India dataset might not have detailed skill information. Consider using only USA data or re-cleaning India data with skill extraction.")
else:
    if country_option == "Compare Both":
        # Calculate skill percentages for both countries
        usa_skills = {}
        india_skills = {}
        
        for col in common_skill_cols:
            skill_name = col.replace('skill_', '').replace('_', ' ').title()
            usa_pct = (df_usa_filtered[col].sum() / len(df_usa_filtered) * 100) if len(df_usa_filtered) > 0 else 0
            india_pct = (df_india_filtered[col].sum() / len(df_india_filtered) * 100) if len(df_india_filtered) > 0 else 0
            
            if usa_pct > 5 or india_pct > 5:  # Only show skills with >5% frequency
                usa_skills[skill_name] = usa_pct
                india_skills[skill_name] = india_pct
        
        # Get top 15 skills (by combined frequency)
        combined_skills = {k: usa_skills.get(k, 0) + india_skills.get(k, 0) for k in set(usa_skills) | set(india_skills)}
        top_skills = sorted(combined_skills.items(), key=lambda x: x[1], reverse=True)[:15]
        top_skill_names = [s[0] for s in top_skills]
        
        # Create comparison dataframe
        skills_comparison = pd.DataFrame({
            'Skill': top_skill_names,
            'USA': [usa_skills.get(s, 0) for s in top_skill_names],
            'India': [india_skills.get(s, 0) for s in top_skill_names]
        })
        
        fig_skills = go.Figure()
        fig_skills.add_trace(go.Bar(
            name='USA',
            x=skills_comparison['Skill'],
            y=skills_comparison['USA'],
            marker_color='#1f77b4'
        ))
        fig_skills.add_trace(go.Bar(
            name='India',
            x=skills_comparison['Skill'],
            y=skills_comparison['India'],
            marker_color='#ff7f0e'
        ))
        
        fig_skills.update_layout(
            title='Top 15 Skills: USA vs India (%)',
            xaxis_title='Skill',
            yaxis_title='% of Jobs',
            barmode='group',
            height=500,
            xaxis={'tickangle': -45}
        )
        st.plotly_chart(fig_skills, use_container_width=True)

    else:
        # Single country view
        df_current = df_usa_filtered if country_option == "USA Only" else df_india_filtered
        current_skill_cols = skill_cols_usa if country_option == "USA Only" else skill_cols_india
        
        if len(current_skill_cols) > 0:
            skill_counts = {}
            for col in current_skill_cols:
                skill_name = col.replace('skill_', '').replace('_', ' ').title()
                count = df_current[col].sum()
                if count > 0:
                    skill_counts[skill_name] = count
            
            top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15])
            
            if len(top_skills) > 0:
                skills_df = pd.DataFrame({
                    'Skill': list(top_skills.keys()),
                    'Count': list(top_skills.values())
                })
                skills_df['Percentage'] = (skills_df['Count'] / len(df_current) * 100).round(1)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        skills_df,
                        x='Count',
                        y='Skill',
                        orientation='h',
                        title='Top 15 Skills',
                        color='Count',
                        color_continuous_scale='Blues' if country_option == "USA Only" else 'Oranges'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Skills Demand")
                    st.dataframe(
                        skills_df[['Skill', 'Percentage']],
                        hide_index=True,
                        height=500
                    )
            else:
                st.info("No skill data available for the selected filters.")
        else:
            st.warning("Skills data not available in this dataset.")

# ===== JOB CATEGORY DISTRIBUTION =====
st.header("📊 Job Role Distribution")

if country_option == "Compare Both":
    col1, col2 = st.columns(2)
    
    with col1:
        usa_cat = df_usa_filtered['job_category'].value_counts().head(10)
        fig_usa_cat = px.pie(
            values=usa_cat.values,
            names=usa_cat.index,
            title='USA: Top 10 Job Categories',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig_usa_cat, use_container_width=True)
    
    with col2:
        india_cat = df_india_filtered['job_category'].value_counts().head(10)
        fig_india_cat = px.pie(
            values=india_cat.values,
            names=india_cat.index,
            title='India: Top 10 Job Categories',
            color_discrete_sequence=px.colors.sequential.Oranges_r
        )
        st.plotly_chart(fig_india_cat, use_container_width=True)

else:
    df_current = df_usa_filtered if country_option == "USA Only" else df_india_filtered
    cat_dist = df_current['job_category'].value_counts().head(10)
    
    fig = px.pie(
        values=cat_dist.values,
        names=cat_dist.index,
        title='Top 10 Job Categories',
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===== TOP LOCATIONS =====
st.header("📍 Top Hiring Locations")

if country_option == "Compare Both":
    col1, col2 = st.columns(2)
    
    with col1:
        usa_loc = df_usa_filtered['location'].value_counts().head(10).reset_index()
        usa_loc.columns = ['Location', 'Jobs']
        
        fig_usa_loc = px.bar(
            usa_loc,
            x='Jobs',
            y='Location',
            orientation='h',
            title='USA: Top 10 States',
            color='Jobs',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_usa_loc, use_container_width=True)
    
    with col2:
        india_loc = df_india_filtered['location'].value_counts().head(10).reset_index()
        india_loc.columns = ['Location', 'Jobs']
        
        fig_india_loc = px.bar(
            india_loc,
            x='Jobs',
            y='Location',
            orientation='h',
            title='India: Top 10 Cities',
            color='Jobs',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_india_loc, use_container_width=True)

else:
    df_current = df_usa_filtered if country_option == "USA Only" else df_india_filtered
    loc_dist = df_current['location'].value_counts().head(10).reset_index()
    loc_dist.columns = ['Location', 'Jobs']
    
    fig = px.bar(
        loc_dist,
        x='Jobs',
        y='Location',
        orientation='h',
        title='Top 10 Locations',
        color='Jobs',
        color_continuous_scale='Blues' if country_option == "USA Only" else 'Oranges'
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===== KEY INSIGHTS =====
st.header("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 Salary Insights")
    if country_option != "India Only":
        usa_median = df_usa_filtered['avg_salary_usd'].median()
        st.write(f"**USA Median:** ${usa_median:.0f}K")
    if country_option != "USA Only":
        india_median = df_india_filtered['avg_salary_lpa'].median()
        st.write(f"**India Median:** ₹{india_median:.1f}L")
    if country_option == "Compare Both":
        ratio = usa_median / (india_median * 1.2)
        st.write(f"**Ratio:** {ratio:.1f}x (absolute)")
        st.write(f"**PPP Adjusted:** ~{ratio/3:.1f}x")

with col2:
    st.subheader("🛠️ Top Skills")
    if country_option == "Compare Both":
        st.write("**Common in Both:**")
        st.write("• Python")
        st.write("• SQL")
        st.write("• AWS/Cloud")
    else:
        df_current = df_usa_filtered if country_option == "USA Only" else df_india_filtered
        skill_counts = {}
        for col in skill_cols:
            skill_counts[col] = df_current[col].sum()
        top_3 = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for skill, count in top_3:
            skill_name = skill.replace('skill_', '').replace('_', ' ').title()
            pct = (count / len(df_current) * 100) if len(df_current) > 0 else 0
            st.write(f"• {skill_name} ({pct:.0f}%)")

with col3:
    st.subheader("📊 Job Market")
    if country_option != "India Only":
        top_cat_usa = df_usa_filtered['job_category'].mode()[0] if len(df_usa_filtered) > 0 else "N/A"
        st.write(f"**USA Top Role:** {top_cat_usa}")
    if country_option != "USA Only":
        top_cat_india = df_india_filtered['job_category'].mode()[0] if len(df_india_filtered) > 0 else "N/A"
        st.write(f"**India Top Role:** {top_cat_india}")

# Footer
st.divider()
st.markdown("""
**📊 Data Sources:**  
- USA: Glassdoor (2,253 jobs)  
- India: Naukri.com (20,000+ jobs)  

**📅 Analysis Period:** 2025  
**👨‍💻 Created by:** [Your Name]  
**🔗 GitHub:** [View Project](https://github.com/yourusername/it-job-market-comparison)

---

**Note:** Salary conversions use approximate rates: 1 LPA ≈ $1.2K USD. PPP adjustment assumes 3x cost of living difference.
""")