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
data = {'Choose your gender': ['Male', 'Female', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male']}
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

st.header("1. Condition Prevalence by Gender")

gender_prevalence = data.groupby('Gender')[['Depression', 'Anxiety', 'PanicAttack']].sum().reset_index()
gender_prevalence_melted = gender_prevalence.melt(
id_vars='Gender', var_name='Condition', value_name='Count'
    )

fig = px.bar(
    gender_prevalence_melted,
    x='Condition',
    y='Count',
    color='Gender',
    barmode='group',
    title='Self-Reported Cases by Gender',
    template='plotly_white',
    color_discrete_map={'Female': '#F67280', 'Male': '#3F78C0'}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    This bar chart illustrates a clear disparity in reported mental health issues between genders. Female students report a substantially higher absolute number of cases across all three conditions (Depression, Anxiety, and Panic Attack). While this may be influenced by enrollment numbers, the gap is significant enough to suggest female students face disproportionate mental distress or are more likely to report it. University support services should consider gender-sensitive outreach and resources to address this pattern effectively.
    """)
