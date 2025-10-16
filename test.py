import streamlit as st
import plotly.express as px
import pandas as pd

# Assuming 'mental_health_df' is loaded elsewhere in your Streamlit app.
# For demonstration, let's create a placeholder DataFrame.
# In a real application, you would replace this with your actual data loading.
data = {'Choose your gender': ['Female', 'Male', 'Female', 'Male','Female', 'Male']}
mental_health_df = pd.DataFrame(data)

# --- Code Conversion Starts Here ---

# Count the occurrences of each gender.
# Plotly Express can often handle this directly if the data is in the right format.
# However, explicitly counting ensures the 'names' and 'values' for the pie chart are correct.
gender_counts = mental_health_df['Choose your gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count'] # Rename columns for clarity in Plotly

# Create a Plotly Pie Chart (equivalent of your matplotlib code)
fig = px.pie(
    gender_counts,
    values='Count',          # The values (counts) for each slice
    names='Gender',          # The labels (gender categories) for each slice
    title='Distribution of Gender',
    color_discrete_sequence=px.colors.sequential.Agsunset, # Choose a color palette
)

# Optional: Customize layout for better appearance (e.g., set uniform text size)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

