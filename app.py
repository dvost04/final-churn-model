!pip install streamlit
import streamlit as st
import pandas as pd

# Data provided by the user, parsed into a DataFrame
data = {
    "Product": ["Daily Fitness", "Healthy Meals", "Mindful Living", "Premium Health", "Wellness Tracker"],
    "Renewal Score": [0.680, 0.683, 0.636, 0.434, 0.618],
    "Primary Focus": ["Retention & Expansion", "Retention & Expansion", "Acquisition", "Acquisition", "Acquisition"],
    "Key Signal": [
        "High renewal rate + expansion ARR exceeds churn",
        "High renewal rate + strong expansion potential",
        "Moderate renewal but new ARR outpaces churn recovery",
        "Very low renewal — must acquire new customers to grow",
        "Lower renewal, new customer revenue drives the business"
    ]
}

df_summary = pd.DataFrame(data)

st.set_page_config(layout="wide")

st.title("Interactive Product Churn Analysis Dashboard")

st.write("Explore the churn characteristics of different products based on the provided summary data.")

# Display the summary DataFrame
st.subheader("Product Churn Summary Data")
st.dataframe(df_summary)

# Interactive elements for filtering and sorting
st.sidebar.header("Filter & Sort Options")

# Filter by Primary Focus
selected_focus = st.sidebar.multiselect(
    "Select Primary Focus:",
    options=df_summary["Primary Focus"].unique(),
    default=df_summary["Primary Focus"].unique()
)

filtered_df = df_summary[df_summary["Primary Focus"].isin(selected_focus)]

# Sort by Renewal Score
sort_order = st.sidebar.radio(
    "Sort by Renewal Score:",
    ('High to Low', 'Low to High'),
    index=0 # Default to High to Low
)

if sort_order == 'High to Low':
    sorted_df = filtered_df.sort_values(by="Renewal Score", ascending=False)
else:
    sorted_df = filtered_df.sort_values(by="Renewal Score", ascending=True)

st.subheader("Filtered and Sorted Results")
st.dataframe(sorted_df)

deployment_instructions = """

st.markdown(deployment_instructions)