import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Visualization"
)

st.header("Genetic Algorithm", divider="gray")


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
