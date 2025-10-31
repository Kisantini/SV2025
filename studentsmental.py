import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration and Data Loading ---

# Define the URL of the raw CSV file
URL = "https://raw.githubusercontent.com/Kisantini/SV2025/refs/heads/main/student_mental_health_data.csv"

st.set_page_config(
    page_title="Interactive Student Mental Health Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use st.cache_data to cache the data loading and cleaning function
@st.cache_data
def load_and_clean_data(data_url):
    """Loads, cleans, and prepares the mental health dataset."""
    try:
        df = pd.read_csv(data_url)

        # 1. Rename columns for simplicity and consistency
        df.rename(columns={
            'Choose your gender': 'Gender',
            'What is your course?': 'Course',
            'Your current year of Study': 'Year',
            'What is your CGPA?': 'CGPA',
            'Marital status': 'Marital_Status',
            'Do you have Depression?': 'Depression',
            'Do you have Anxiety?': 'Anxiety',
            'Do you have Panic attack?': 'Panic_Attack',
            'Did you seek any specialist for a treatment?': 'Treatment_Sought'
        }, inplace=True)

        # 2. Clean and standardize categorical columns
        df['Gender'] = df['Gender'].str.title()
        df['Year'] = df['Year'].str.lower().str.replace('year ', 'Year ').replace({'Year 1': 'Year 1', 'Year 2': 'Year 2', 'Year 3': 'Year 3', 'year 4': 'Year 4'})
        df['CGPA'] = df['CGPA'].str.strip()
        
        # 3. Create a combined mental health issue count (0 to 3)
        issue_map = {'Yes': 1, 'No': 0}
        df['Depression_Score'] = df['Depression'].map(issue_map)
        df['Anxiety_Score'] = df['Anxiety'].map(issue_map)
        df['Panic_Attack_Score'] = df['Panic_Attack'].map(issue_map)
        
        df['Issue_Count'] = df['Depression_Score'] + df['Anxiety_Score'] + df['Panic_Attack_Score']

        # 4. Create binary flag for "Any Issue"
        df['Any_Issue'] = df['Issue_Count'].apply(lambda x: 'Yes' if x > 0 else 'No')
        
        # 5. Drop the row with NaN Age
        df.dropna(subset=['Age'], inplace=True)

        return df

    except Exception as e:
        st.error(f"Failed to process data. Error: {e}")
        return pd.DataFrame()

github_df = load_and_clean_data(URL)

# --- Streamlit Dashboard Layout ---

st.title("Interactive Student Mental Health Analysis 🧠")
st.markdown("This dashboard uses **Plotly** for dynamic and engaging visualizations of student mental health survey data.")

if github_df.empty:
    st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='PLO 2', value=f'3.5',help='PLO 2: Cognitive skill',border=True)
col2.metric(label='PLO 3', value=f'3.5',help='PLO 3: Digital skill',border=True)
col3.metric(label='PLO 4', value=f'4.0',help='PLO 4: Interpersonal skill',border=True)
col1.metric(label='PLO 5', value=f'4.3',help='PLO 2: Communication skill',border=True)

# --- Visualization Functions ---

def create_viz_block(title, chart, interpretation):
    """Helper function to display chart and interpretation in a block."""
    st.subheader(f"{title.split(':')[0]}: {title.split(': ')[1]}")
    st.plotly_chart(chart, use_container_width=True)
    st.markdown(f"**Interpretation:** {interpretation}")
    st.markdown("---")

# ----------------------------------------------------------------------
# VISUALIZATION 1 (Pie Chart): Proportional Distribution of Specific Issues
# ----------------------------------------------------------------------
title_1 = "1 (Pie Chart): Proportion of Students Reporting Each Specific Mental Health Issue"
df_melt = github_df[['Depression', 'Anxiety', 'Panic_Attack']].melt(
    value_vars=['Depression', 'Anxiety', 'Panic_Attack'], var_name='Issue_Type', value_name='Reported'
)
df_issue_counts = df_melt[df_melt['Reported'] == 'Yes']['Issue_Type'].value_counts().reset_index()
df_issue_counts.columns = ['Issue_Type', 'Count']

fig_1 = px.pie(
    df_issue_counts, 
    values='Count', 
    names='Issue_Type', 
    title='Relative Frequency of Reported Issues',
    color_discrete_sequence=px.colors.qualitative.D3
)
fig_1.update_traces(textposition='inside', textinfo='percent+label')

interpretation_1 = (
    "This Pie Chart clearly illustrates the relative frequency of the three specific mental health concerns reported by the students. "
    "**Anxiety** accounts for the largest share of reported issues, suggesting it is the most prevalent struggle in this sample. "
    "Depression is the second most common, while Panic Attacks are reported the least frequently. "
    "The visualization confirms that interventions focused on general anxiety management would address the most common challenge faced by these students."
)
create_viz_block(title_1, fig_1, interpretation_1)


# ----------------------------------------------------------------------
# VISUALIZATION 2 (Violin Plot): Age Distribution by Depression Status
# ----------------------------------------------------------------------
title_2 = "2 (Violin Plot): Student Age Distribution vs. Depression Status"

fig_2 = px.violin(
    github_df, 
    y="Age", 
    x="Depression", 
    color="Depression", 
    box=True, # Show box plot inside the violin
    points="all", # Show all data points
    title="Age Distribution for Students With and Without Depression",
    labels={"Depression": "Reported Depression", "Age": "Age of Student"},
    color_discrete_map={'Yes':'#EF553B', 'No':'#00CC96'}
)
fig_2.update_layout(showlegend=False)

interpretation_2 = (
    "The Violin Plot displays the distribution of student ages, segmented by whether they reported having Depression. "
    "The most notable insight is that the median age (indicated by the box plot line) is slightly **higher for students reporting Depression (Yes)** compared to those reporting No Depression. "
    "This may indicate that older students (e.g., those in their final years or non-traditional students) are slightly more likely to experience or report depressive symptoms. "
    "The spread of ages (violin shape) is wide for both groups, suggesting that age alone is not a primary determining factor."
)
create_viz_block(title_2, fig_2, interpretation_2)


# ----------------------------------------------------------------------
# VISUALIZATION 3 (Grouped Bar Chart): Treatment Seeking Across Academic Years
# ----------------------------------------------------------------------
title_3 = "3 (Grouped Bar Chart): Treatment Seeking Behavior by Academic Year"

# Calculate counts for plotting
df_treatment_year = github_df.groupby(['Year', 'Treatment_Sought']).size().reset_index(name='Count')

fig_3 = px.bar(
    df_treatment_year,
    x='Year',
    y='Count',
    color='Treatment_Sought',
    barmode='group',
    category_orders={'Year': ['Year 1', 'Year 2', 'Year 3', 'Year 4']},
    title='Absolute Count of Treatment Sought by Academic Year',
    labels={'Year': 'Academic Year', 'Count': 'Number of Students'},
    color_discrete_map={'Yes':'#636EFA', 'No':'#B0C4DE'}
)

interpretation_3 = (
    "This Grouped Bar Chart compares the absolute number of students who sought treatment against those who did not, across all academic years. "
    "A clear pattern emerges: the vast majority of students across all years, especially those in **Year 1 and Year 2**, report **not** having sought treatment. "
    "Crucially, Year 4 students show the lowest counts overall, likely due to fewer respondents in that category, but the ratio of Yes/No seekers remains low. "
    "This visualization highlights a significant gap where mental health issues may exist but professional help is generally not being accessed by the student body."
)
create_viz_block(title_3, fig_3, interpretation_3)


# ----------------------------------------------------------------------
# VISUALIZATION 4 (Sunburst Chart): Hierarchical Issues by Year and Gender
# ----------------------------------------------------------------------
title_4 = "4 (Sunburst Chart): Breakdown of Students with 'Any Mental Health Issue' by Academic Year and Gender"

# Filter for students with issues
df_sunburst = github_df[github_df['Any_Issue'] == 'Yes']

fig_4 = px.sunburst(
    df_sunburst,
    path=['Year', 'Gender'], # Hierarchy: Year -> Gender
    title='Students Reporting Any Issue: Hierarchical Breakdown by Year and Gender',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={'parent': 'Academic Year', 'Gender': 'Gender'}
)
fig_4.update_layout(margin=dict(t=50, l=0, r=0, b=0))

interpretation_4 = (
    "The Sunburst Chart provides a nested, proportional view of students reporting any mental health issue, first by their academic year, then by gender. "
    "The outer ring's largest segment belongs to **Year 2 Female** students, indicating this subgroup has the highest absolute number of reported issues in the dataset. "
    "Female students consistently dominate the reports within every year group, reflecting the high gender imbalance of the full dataset. "
    "This hierarchy is useful for targeting outreach, suggesting Year 2 females are a priority group for support resources."
)
create_viz_block(title_4, fig_4, interpretation_4)


# ----------------------------------------------------------------------
# VISUALIZATION 5 (Box Plot): Issue Count Score Distribution by CGPA
# ----------------------------------------------------------------------
title_5 = "5 (Box Plot): Distribution of Mental Health Issue Score (0-3) Across CGPA Categories"

# Order the CGPA categories logically
cgpa_order = ['0 - 1.99', '2.00 - 2.49', '2.50 - 2.99', '3.00 - 3.49', '3.50 - 4.00']

fig_5 = px.box(
    github_df,
    x='CGPA',
    y='Issue_Count',
    color='CGPA',
    category_orders={'CGPA': cgpa_order},
    title="Mental Health Issue Severity (Count) by Academic Performance (CGPA)",
    labels={'CGPA': 'CGPA Range', 'Issue_Count': 'Number of Reported Issues (0=None, 3=All)'}
)
fig_5.update_yaxes(tickvals=[0, 1, 2, 3], ticktext=['0', '1', '2', '3']) # Fix y-axis ticks

interpretation_5 = (
    "This Box Plot examines the median and spread of the 'Issue Count' (a proxy for severity, from 0 to 3) across CGPA ranges. "
    "The median issue count is notably low (0 or 1) across all CGPA groups, suggesting most students report zero or only one issue. "
    "However, the highest median issue count appears in the mid-range **3.00 - 3.49** category, supporting the earlier finding that pressure to maintain above-average grades might increase stress. "
    "The fact that the 3.50 - 4.00 category shows a lower median and narrower distribution suggests that the top academic performers are generally the most mentally resilient in this sample."
)
create_viz_block(title_5, fig_5, interpretation_5)
