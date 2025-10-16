import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load your data
mental_health_df = pd.read_csv("student_mental_health_data.csv")

# Count the occurrences of each gender
gender_counts = mental_health_df['Choose your gender'].value_counts()

# Streamlit App
st.title('Mental Health Data Visualization')
st.subheader('Gender Distribution')

# Create a pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax.set_title('Distribution of Gender')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart in Streamlit
st.pyplot(fig)
