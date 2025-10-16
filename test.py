import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load your data
mental_health_df = pd.read_csv("student_mental_health_data.csv")

st.header("Gender Distribution in Survey Respondents")

# Create a Plotly Pie Chart
# This is the line that was failing, now using the properly formatted DataFrame
fig = px.pie(
    gender_data_for_plot,
    values='Count',
    names='Gender',
    title='Distribution of Gender',
    color_discrete_sequence=px.colors.sequential.RdBu,
    hole=0.3 # Creates a donut chart
)

# Optional: Customize the appearance for clarity
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add text below the graph
st.caption("Figure 1: This chart visualizes the proportion of each gender category among the survey participants.")
st.write(
    """
    **Data Note:** Plotly requires the data to be in a structured format (a DataFrame) with distinct columns 
    for the slice size (`values`) and the slice labels (`names`). The error likely occurred because the 
    DataFrame was not correctly constructed or named before passing it to `px.pie()`.
    """
)
