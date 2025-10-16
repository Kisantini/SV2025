import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Visualization"
)

st.header("Student Mental Health Year 1", divider="gray")


# --- Assuming 'mental_health_df' is already loaded and available in your Streamlit app ---
# Placeholder for demonstration. Replace with your actual data loading.
# Example DataFrame structure for demonstration purposes:
data = {'Choose your gender': ['Male', 'Female', 'Male', 'Non-binary', 'Female', 'Male', 'Female', 'Male']}
mental_health_df = pd.DataFrame(data)
# --------------------------------------------------------------------------------------


# Count the occurrences of each gender
gender_counts = mental_health_df['Choose your gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count'] # Rename columns for clarity in Plotly

# Create a Plotly Pie Chart
# Plotly Express is often the simplest way to create standard plots
fig = px.pie(
    gender_counts,
    values='Count',
    names='Gender',
    title='Distribution of Gender',
    # Optional: Customize the appearance
    color_discrete_sequence=px.colors.sequential.RdBu, # Example color sequence
    hole=0.3 # Optional: makes it a donut chart
)

# Optional: Further customize layout
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# You can also display the raw data used for the chart
st.write("### Gender Counts")
st.dataframe(gender_counts)

# --- Assuming 'mental_health_df' is already loaded and available in your Streamlit app ---
# Placeholder for demonstration. Replace with your actual data loading.
data = {
    'Age': [25, 30, 25, 40, 30, 25, 40, 30, 25, 40],
    'Do you have Depression?': ['Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No']
}
mental_health_df = pd.DataFrame(data)
# --------------------------------------------------------------------------------------

# 1. Prepare the data: Calculate the counts for each Age and Depression combination
# The original sns.countplot implicitly does this. For Plotly, we explicitly count and group.
age_depression_counts = mental_health_df.groupby(['Age', 'Do you have Depression?']).size().reset_index(name='Count')


# 2. Create the Plotly Bar Chart
fig = px.bar(
    age_depression_counts,
    x='Age',                             # Column for the x-axis
    y='Count',                           # Column for the height of the bars
    color='Do you have Depression?',     # Column to color/group the bars (equivalent to 'hue')
    barmode='group',                     # Ensures the bars are grouped side-by-side
    title='Relationship between Age and Depression',
    labels={'Age': 'Age of Respondent', 'Count': 'Number of Respondents'},
    # Optional: Customize the colors (e.g., matching the 'viridis' feel)
    color_discrete_map={'Yes': '#440154', 'No': '#21908d'} # Example colors
)

# Optional: Further customize the layout for better appearance
fig.update_layout(
    xaxis={'categoryorder':'category ascending'} # Ensures 'Age' is sorted correctly
)


# 3. Display the plot in Streamlit
st.title("Mental Health Survey Analysis")
st.plotly_chart(fig, use_container_width=True)

# You can also display the raw count data
st.write("### Count Data Used for Plot")
st.dataframe(age_depression_counts)
