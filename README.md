# 📊 Data Jobs Market Analysis 2025



A comprehensive analysis of **2,253 data analyst and data scientist job postings** from Glassdoor, uncovering salary trends, in-demand skills, and hiring patterns in the US data job market.

## 🎯 Project Objectives

- Analyze **salary distributions** across seniority levels and geographic locations
- Identify the **most in-demand technical skills** for data professionals
- Discover **top hiring companies** and industry trends
- Provide **actionable insights** for job seekers entering the data field

## 🔍 Key Findings

### 💰 Salary Insights
- **Overall Median Salary:** $77K
- **Junior Level:** $62K median
- **Mid-Level:** $78K median
- **Senior Level:** $105K median
- **Salary Growth:** 70% increase from junior to senior level

### 🛠️ Top 10 Most In-Demand Skills
1. **SQL** (61.7% of jobs) - Database querying is essential
2. **Excel** (60.6% of jobs) - Still highly relevant for data analysis
3. **Statistics** (37.4% of jobs) - Statistical knowledge is crucial
4. **Python** (31.5% of jobs) - Key programming language
5. **Tableau** (27.5% of jobs) - Leading visualization tool
6. **SAS** (18.3% of jobs) - Important in certain industries
7. **ETL** (17.6% of jobs) - Data pipeline skills valued
8. **R** (15.0% of jobs) - Statistical programming
9. **Data Visualization** (14.9% of jobs) - Critical for communication
10. **Git** (13.5% of jobs) - Version control is increasingly important

**Key Takeaway:** SQL + Excel + Python form the essential foundation. Master these three before specializing.

### 📍 Geographic Distribution
**Top 5 States:**
1. **California** - 20% of all jobs, $85K median salary
2. **New York** - 12% of jobs, $82K median salary
3. **Texas** - 9% of jobs, $75K median salary
4. **Massachusetts** - 7% of jobs, $88K median salary
5. **Illinois** - 6% of jobs, $73K median salary

**Highest Paying States:**
1. California: $85K
2. Massachusetts: $88K
3. New York: $82K
4. Washington: $84K
5. Virginia: $79K

### 🏢 Key Observations
- **Skill Combinations:** 58% of jobs require SQL + Excel together
- **Seniority Distribution:** 45% Mid-Level, 35% Senior, 20% Junior
- **Industries:** IT Services, Finance, and Healthcare dominate data hiring
- **Company Size:** Large companies (1000+ employees) offer 15% higher salaries

## 🚀 Live Dashboard

**🔗 [View Interactive Dashboard](your-streamlit-link-here)**

The dashboard features:
- Real-time filtering by seniority, location, and salary
- Interactive salary distribution charts
- Geographic heatmaps
- Skill demand visualizations
- Company and industry breakdowns

![Dashboard Preview](outputs/plots/dashboard_preview.png)

## 🛠️ Tech Stack

**Data Collection & Processing:**
- Python 3.8+
- Pandas for data manipulation
- NumPy for numerical operations
- Regular expressions for text parsing

**Analysis & Visualization:**
- Matplotlib for static plots
- Seaborn for statistical visualizations
- Plotly for interactive charts

**Dashboard & Deployment:**
- Streamlit for web application
- Plotly Express for interactive elements

## 📁 Project Structure

```
job-market-analysis/
├── data/
│   ├── raw/                    # Original Glassdoor dataset
│   └── processed/              # Cleaned data (jobs_cleaned.csv)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis_and_viz.ipynb
├── outputs/
│   └── plots/                  # Generated visualizations
├── app.py                      # Streamlit dashboard
├── requirements.txt            # Python dependencies
└── README.md
```

## 📊 Methodology

### 1. Data Collection
- **Source:** Glassdoor job postings dataset (Kaggle)
- **Sample Size:** 2,253 jobs
- **Job Types:** Data Analyst, Data Scientist, Business Analyst
- **Data Points:** Job title, company, salary, location, description, ratings

### 2. Data Cleaning & Preprocessing
- Extracted salary ranges from text (e.g., "$37K-$66K")
- Parsed company ratings and cleaned company names
- Standardized location data (city and state)
- Created seniority classifications from job titles
- **Skill Extraction:** Used keyword matching on job descriptions to identify 25+ technical skills
- Removed duplicates and handled missing values

### 3. Exploratory Data Analysis
- Salary distribution analysis by seniority and location
- Skill frequency analysis across all job postings
- Geographic trend identification
- Industry and company size correlations with salary
- Skill co-occurrence patterns

### 4. Visualization & Dashboard
- Created 7 publication-quality static visualizations
- Built interactive Streamlit dashboard with filters
- Implemented responsive charts using Plotly
- Deployed for public access

## 💻 How to Run This Project

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/job-market-analysis.git
cd job-market-analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download the dataset**
- Get the dataset from [Kaggle](https://www.kaggle.com)
- Place `jobs_raw.csv` in `data/raw/` folder

4. **Run the analysis notebooks** (optional)
```bash
jupyter notebook
```
Open and run notebooks in order: 01, 02, 03

5. **Launch the dashboard**
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📦 Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.11.0
streamlit>=1.25.0
jupyter>=1.0.0
```

## 📈 Sample Visualizations

### Top Skills Distribution
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/fb668f28-1e36-4873-8717-3191a76f4cbb" />


### Salary Analysis
<img width="1013" height="500" alt="image" src="https://github.com/user-attachments/assets/615663ac-2032-4cf0-9812-cd4ec3336dc7" />



### Geographic Distribution
<img width="1025" height="506" alt="image" src="https://github.com/user-attachments/assets/38504e3c-5b50-4b69-b08b-29d994707279" />

## 🎓 Key Learnings & Skills Demonstrated

### Technical Skills
- **Data Wrangling:** Cleaned messy text data (salaries, locations, job titles)
- **Text Processing:** Extracted structured information from unstructured job descriptions
- **Feature Engineering:** Created skill indicators and seniority classifications
- **Statistical Analysis:** Calculated distributions, correlations, and trends
- **Data Visualization:** Created clear, compelling visualizations
- **Web Development:** Built interactive dashboard with Streamlit

### Domain Knowledge
- Understanding of the data job market landscape
- Familiarity with data tools and technologies
- Knowledge of hiring trends and salary expectations

### Soft Skills
- Problem-solving: Tackled data quality issues
- Communication: Presented findings clearly through visualizations
- Project Management: Organized end-to-end data analysis project

## 🔮 Future Enhancements

- [ ] Time-series analysis tracking trends over months/years
- [ ] NLP analysis of job descriptions for deeper insights
- [ ] Machine learning model to predict salaries based on skills
- [ ] Skill co-occurrence network visualization
- [ ] Job recommendation system based on user skills
- [ ] Automated data collection pipeline for real-time updates
- [ ] Add remote vs. on-site analysis
- [ ] Compare data roles (Analyst vs. Scientist vs. Engineer)

## 💡 Insights for Job Seekers

### If You're Just Starting:
1. **Focus on the core three:** SQL, Excel, Python (in that order)
2. **Build projects** that demonstrate these skills
3. **Target junior roles** in large companies or startups
4. **Consider geography:** California and Massachusetts pay premium salaries

### To Stand Out:
1. **Add visualization skills:** Tableau or Power BI
2. **Learn version control:** Git/GitHub
3. **Understand statistics:** Not just tools, but statistical reasoning
4. **Develop communication skills:** Present your findings clearly

### Salary Negotiation:
- Research location-specific salaries (our dashboard helps!)
- Senior roles pay 70% more than junior
- Large companies (1000+) typically pay more
- Tech industry offers highest salaries for data roles


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Source:** Glassdoor (via Kaggle dataset)
- **Inspiration:** Data job seekers looking to understand the market
- **Tools:** Thanks to the open-source community for amazing libraries

---



## 📊 Project Stats

- **Lines of Code:** ~1,200
- **Data Points Analyzed:** 2,253 jobs × 16 features = 36,048 data points
- **Visualizations Created:** 7 static + 10 interactive
- **Skills Tracked:** 25+ technical skills
- **Time to Complete:** ~30 hours

**This project demonstrates:** Data collection → Cleaning → Analysis → Visualization → Deployment
