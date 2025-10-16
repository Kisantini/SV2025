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

print("--- Visualization: Course of Study vs. Gender ---")
plt.figure(figsize=(14, 8))

# Generate the countplot
sns.countplot(
    y='What is your course?', 
    hue='Choose your gender', 
    data=mental_health_df, 
    # Order bars by the total count of students in that course
    order=mental_health_df['What is your course?'].value_counts().index, 
    palette='viridis'
)

plt.title('Relationship between Course of Study and Gender', fontsize=16, pad=20)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Course of Study', fontsize=14)
plt.legend(title='Gender', loc='lower right')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# --- 3. Interpretation ---
print("\n--- Interpretation ---")
interpretation = """
This countplot clearly illustrates the gender distribution within the different academic courses represented in the dataset (N=41).

**Key Findings:**

1.  **Overall Gender Skew:** The sample has a significant overall skew towards **Female** respondents, which is reflected across most courses.
2.  **Most Represented Courses:** The largest groups—**Engineering** (9 Female, 2 Male) and **BCS** (8 Female, 2 Male)—are female-dominated, reflecting the broader sample bias.
3.  **Female-Only Representation:** Several smaller courses, including Psychology, Banking Studies, ENM, and others, show participants exclusively from the female demographic in this dataset.

**Conclusion:**

The data suggests that the survey successfully captured the perspective of female students across various academic programs, but caution is advised when generalizing findings due to the pronounced underrepresentation of male students.
"""
print(interpretation)
