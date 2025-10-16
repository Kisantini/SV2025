import streamlit as st
import pandas as pd

# Define the URL of the raw CSV file
url = "https://raw.githubusercontent.com/Kisantini/SV2025/refs/heads/main/student_mental_health_data.csv"

st.title("Student Mental Health Data Viewer 🧠")
st.subheader("Data Loaded from GitHub CSV")

# Use st.cache_data to cache the data loading function.
# This makes the app load much faster and prevents re-downloading the data.
@st.cache_data
def load_data(data_url):
    """Loads the CSV data into a pandas DataFrame."""
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        # Display an error if loading fails
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Load the data
github_df = load_data(url)

# Display the data and information if the DataFrame is not empty
if not github_df.empty:
    st.success("Data loaded successfully!")
    st.write(f"DataFrame shape: **{github_df.shape}**")

    st.markdown("---")

    st.subheader("First 10 Rows of the Data")
    # Display the DataFrame using st.dataframe for an interactive table
    st.dataframe(github_df.head(10))

    st.markdown("---")

    st.subheader("Data Information (Columns and Types)")
    # Use a text area to display the DataFrame info
    st.text(github_df.info(buf=None))

else:
    st.error("Could not load data. Please check the URL and file availability.")
