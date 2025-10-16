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

import streamlit as st
import plotly.express as px
import pandas as pd

# --- Assuming 'mental_health_df' and 'fig' (the Plotly figure) are already defined ---
# (Using placeholder code for context)
data = {
    'Age': [25, 30, 25, 40, 30, 25, 40, 30, 25, 40],
    'Do you have Depression?': ['Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No']
}
mental_health_df = pd.DataFrame(data)
age_depression_counts = mental_health_df.groupby(['Age', 'Do you have Depression?']).size().reset_index(name='Count')
fig = px.bar(age_depression_counts, x='Age', y='Count', color='Do you have Depression?', barmode='group', title='Relationship between Age and Depression')
# --------------------------------------------------------------------------------------


# 1. Display the Plotly chart
st.plotly_chart(fig, use_container_width=True)

# 2. Add text directly below the graph using Streamlit's text functions
# Use different functions depending on the style and size you want:

# For a small, descriptive caption/note
st.caption("Figure 1: This bar chart shows the distribution of depression diagnoses across different age groups in the survey.")

# For a general block of text or an observation
st.write("Observation: The age group 25-30 appears to have the highest reported count of depression in this dataset.")

# For a slightly emphasized note
st.markdown("**Note:** This is preliminary data and does not imply causation.")
