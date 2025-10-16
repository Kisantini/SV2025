import streamlit as st
import pandas as pd
import altair as alt

# --- Configuration and Data Loading ---

# Define the URL of the raw CSV file
URL = "https://raw.githubusercontent.com/Kisantini/SV2025/refs/heads/main/student_mental_health_data.csv"

st.set_page_config(
    page_title="Student Mental Health Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use st.cache_data to cache the data loading and cleaning function
@st.cache_data
def load_and_clean_data(data_url):
    """Loads, cleans, and prepares the mental health dataset."""
    try:
        df = pd.read_csv(data_url)

        # 1. Rename columns for simplicity and consistency based on inspection
        df.rename(columns={
            'Choose your gender': 'Gender',
            'Your current year of Study': 'Year',
            'What is your CGPA?': 'CGPA',
            'Marital status': 'Marital_Status',
            'Do you have Depression?': 'Depression',
            'Do you have Anxiety?': 'Anxiety',
            'Do you have Panic attack?': 'Panic_Attack',
            'Did you seek any specialist for a treatment?': 'Treatment_Sought'
        }, inplace=True)

        # 2. Clean 'Gender' column (convert to title case for consistency)
        df['Gender'] = df['Gender'].str.title()

        # 3. Clean 'Year' column (standardize capitalization, e.g., 'Year 1' to 'year 1')
        df['Year'] = df['Year'].str.lower().str.replace('year ', 'Year ')
        
        # 4. Clean 'CGPA' column (strip whitespace)
        df['CGPA'] = df['CGPA'].str.strip()

        # 5. Create a combined mental health issue column
        mental_health_cols = ['Depression', 'Anxiety', 'Panic_Attack']
        df['Any_Mental_Health_Issue'] = df[mental_health_cols].apply(
            lambda row: 'Yes' if (row == 'Yes').any() else 'No', axis=1
        )
        
        # Drop the row with NaN Age (only one in this dataset)
        df.dropna(subset=['Age'], inplace=True)
        
        return df

    except Exception as e:
        st.error(f"Failed to process data. Error: {e}")
        return pd.DataFrame()

github_df = load_and_clean_data(URL)

# --- Streamlit Dashboard Layout ---

st.title("Student Mental Health Dashboard 📊")
st.markdown("Exploring the relationship between student demographics, academic status, and reported mental health issues (Depression, Anxiety, Panic Attacks).")

if github_df.empty:
    st.stop()

st.sidebar.header("Dashboard Controls")
show_data = st.sidebar.checkbox("Show Raw Data Table", False)

if show_data:
    st.header("Raw Data Preview")
    st.dataframe(github_df)
    st.markdown("---")


# --- Visualization Functions ---

def create_viz_block(title, chart, interpretation):
    """Helper function to display chart and interpretation in a block."""
    st.subheader(f"Viz #{title.split(':')[0]}: {title.split(': ')[1]}")
    st.altair_chart(chart, use_container_width=True)
    st.markdown(f"**Interpretation:** {interpretation}")
    st.markdown("---")

# ----------------------------------------------------------------------
# VISUALIZATION 1: Gender Distribution
# ----------------------------------------------------------------------
title_1 = "1: Gender Distribution of Respondents"
df_gender = github_df['Gender'].value_counts().reset_index()
df_gender.columns = ['Gender', 'Count']

chart_1 = alt.Chart(df_gender).mark_bar().encode(
    x=alt.X('Count'),
    y=alt.Y('Gender', sort='-x'),
    color=alt.Color('Gender', scale=alt.Scale(domain=['Female', 'Male'], range=['#90EE90', '#ADD8E6'])),
    tooltip=['Gender', 'Count']
).properties(
    title=title_1
)

interpretation_1 = (
    "The dataset exhibits a clear imbalance in respondents, with a significantly higher number of **Female** students participating compared to Male students. "
    "This imbalance means that any percentage comparison between genders must be interpreted with caution, as the absolute numbers are skewed. "
    "For instance, even if the absolute number of reported issues is similar, the underlying population proportion (Female vs. Male) in the dataset is unequal. "
    "This initial view highlights a potential sampling bias."
)
create_viz_block(title_1, chart_1, interpretation_1)


# ----------------------------------------------------------------------
# VISUALIZATION 2: Mental Health Prevalence by Gender
# ----------------------------------------------------------------------
title_2 = "2: Percentage of Students Reporting ANY Mental Health Issue, by Gender"
df_prevalence_gender = github_df.groupby('Gender')['Any_Mental_Health_Issue'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()
df_prevalence_gender_yes = df_prevalence_gender[df_prevalence_gender['Any_Mental_Health_Issue'] == 'Yes']

chart_2 = alt.Chart(df_prevalence_gender_yes).mark_bar().encode(
    x=alt.X('Percentage', axis=alt.Axis(title='Percentage of Group Reporting Issue (%)')),
    y=alt.Y('Gender', sort='-x'),
    color=alt.Color('Gender', scale=alt.Scale(domain=['Female', 'Male'], range=['#FF6347', '#4682B4'])),
    tooltip=['Gender', alt.Tooltip('Percentage', format='.1f')]
).properties(
    title=title_2
)

interpretation_2 = (
    "When normalized by group size, the data shows that a higher **percentage of Female students** (around 54%) report experiencing at least one mental health issue (Depression, Anxiety, or Panic Attack) compared to Male students (around 30%). "
    "This suggests that Female students in this sample report disproportionately higher rates of mental health struggles. "
    "This finding is consistent with broader epidemiological studies that often observe higher self-reported rates of anxiety and depression in young women."
)
create_viz_block(title_2, chart_2, interpretation_2)


# ----------------------------------------------------------------------
# VISUALIZATION 3: Mental Health Issues vs. Academic Performance (CGPA)
# ----------------------------------------------------------------------
title_3 = "3: Any Mental Health Issue Prevalence Across CGPA Categories"
df_cgpa = github_df.groupby('CGPA')['Any_Mental_Health_Issue'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()
df_cgpa_yes = df_cgpa[df_cgpa['Any_Mental_Health_Issue'] == 'Yes']

# Order the CGPA categories logically
cgpa_order = ['0 - 1.99', '2.00 - 2.49', '2.50 - 2.99', '3.00 - 3.49', '3.50 - 4.00']
cgpa_order_label = ['0-1.99', '2.00-2.49', '2.50-2.99', '3.00-3.49', '3.50-4.00']

chart_3 = alt.Chart(df_cgpa_yes).mark_bar().encode(
    x=alt.X('CGPA', sort=cgpa_order, axis=alt.Axis(title="CGPA Range", labels=cgpa_order_label)),
    y=alt.Y('Percentage', axis=alt.Axis(title='Percentage Reporting Issue (%)')),
    color=alt.value('#1E90FF'), # Solid color for simplicity
    tooltip=['CGPA', alt.Tooltip('Percentage', format='.1f')]
).properties(
    title=title_3
)

interpretation_3 = (
    "The data reveals an inverse relationship between academic performance (CGPA) and reported mental health issues, but it is not perfectly linear. "
    "Students in the highest CGPA bracket (**3.50 - 4.00**) report the lowest rate of issues (around 32%), suggesting academic success may correlate with better mental resilience or lower stress levels. "
    "Conversely, the group with a mid-range CGPA of **3.00 - 3.49** shows the highest prevalence (around 53%). "
    "This suggests that pressure to maintain above-average grades, rather than low grades alone, might be a significant stressor for students in this sample."
)
create_viz_block(title_3, chart_3, interpretation_3)


# ----------------------------------------------------------------------
# VISUALIZATION 4: Distribution of Specific Mental Health Issues
# ----------------------------------------------------------------------
title_4 = "4: Distribution of Specific Reported Mental Health Issues (Depression, Anxiety, Panic Attacks)"
# Unpivot the three mental health columns for easier plotting
df_melt = github_df[['Depression', 'Anxiety', 'Panic_Attack']].melt(
    value_vars=['Depression', 'Anxiety', 'Panic_Attack'],
    var_name='Issue_Type',
    value_name='Reported'
)
# Count only the 'Yes' responses
df_issue_count = df_melt[df_melt['Reported'] == 'Yes']['Issue_Type'].value_counts().reset_index()
df_issue_count.columns = ['Issue_Type', 'Count']

chart_4 = alt.Chart(df_issue_count).mark_bar().encode(
    x=alt.X('Count'),
    y=alt.Y('Issue_Type', sort='-x', title="Mental Health Issue"),
    color=alt.Color('Issue_Type', scale=alt.Scale(range=['#FFD700', '#FFA07A', '#F08080'])),
    tooltip=['Issue_Type', 'Count']
).properties(
    title=title_4
)

interpretation_4 = (
    "Among the three specific issues surveyed, **Anxiety** is the most frequently reported concern, with the highest absolute count among students. "
    "Depression follows as the second most common, and Panic Attacks are reported least frequently. "
    "This hierarchy suggests that general feelings of worry and anxiousness are the primary mental health struggle for this student population. "
    "Interventions aimed at stress management and anxiety reduction are likely to reach the largest number of students based on these reported frequencies."
)
create_viz_block(title_4, chart_4, interpretation_4)


# ----------------------------------------------------------------------
# VISUALIZATION 5: Treatment Seeking Behavior by Marital Status
# ----------------------------------------------------------------------
title_5 = "5: Proportion of Students Who Sought Treatment, Grouped by Marital Status"
df_treatment = github_df.groupby('Marital_Status')['Treatment_Sought'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()
df_treatment_yes = df_treatment[df_treatment['Treatment_Sought'] == 'Yes']

chart_5 = alt.Chart(df_treatment_yes).mark_bar().encode(
    x=alt.X('Percentage', axis=alt.Axis(title='Percentage of Group Seeking Treatment (%)')),
    y=alt.Y('Marital_Status', title="Marital Status", sort='-x'),
    color=alt.Color('Marital_Status', scale=alt.Scale(range=['#48D1CC', '#808080'])),
    tooltip=['Marital_Status', alt.Tooltip('Percentage', format='.1f')]
).properties(
    title=title_5
)

interpretation_5 = (
    "The data shows a clear distinction in treatment-seeking behavior based on marital status. "
    "Students who report being **Married** show a dramatically higher tendency to have sought professional treatment (nearly 50% of the group) compared to those who are Single (around 12%). "
    "While the number of married students is small, this difference is striking. "
    "This insight suggests that having a spouse/partner may provide a stronger support system or motivation to address mental health issues professionally, or that the stressors of married life/student life combination necessitate professional help more frequently."
)
create_viz_block(title_5, chart_5, interpretation_5)
