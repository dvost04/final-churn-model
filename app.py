import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# --- 1. Load the main dataset (replace with your actual data loading method for deployment) ---
# For local Colab execution, you might have df from files.upload() or a local path.
# For Render deployment, assume 'ASSIGNMENT2REDO_2026-07-26-2252 .csv' is in the same directory.
try:
    df = pd.read_csv('ASSIGNMENT2REDO_2026-07-26-2252.csv')
except FileNotFoundError:
    st.error("Data file 'ASSIGNMENT2REDO_2026-07-26-2252.csv' not found. Please ensure it's in the same directory as app.py for deployment.")
    st.stop()

# --- 2. Train the Predictive Model (same as before) ---
X = df.drop(['CUSTOMER_ID', 'RENEWED'], axis=1)
y = df['RENEWED']

categorical_features = X.select_dtypes(include=['object']).columns
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model_pipeline.fit(X_train, y_train)

# --- 3. Streamlit Application Layout and Logic ---
st.set_page_config(layout="wide")
st.title("Interactive Customer Renewal Prediction Dashboard")

st.markdown("Adjust the customer attributes below to predict their renewal probability and churn rate.")

# Sidebar for user input
st.sidebar.header("Customer Attributes for Prediction")

# Collect user input for numerical features
input_total_sessions = st.sidebar.slider('Total Sessions', int(df['TOTAL_SESSIONS'].min()), int(df['TOTAL_SESSIONS'].max()), int(df['TOTAL_SESSIONS'].median()))
input_gross_session_length = st.sidebar.slider('Gross Session Length', int(df['GROSS_SESSION_LENGTH'].min()), int(df['GROSS_SESSION_LENGTH'].max()), int(df['GROSS_SESSION_LENGTH'].median()))
input_active_days = st.sidebar.slider('Active Days', int(df['ACTIVE_DAYS'].min()), int(df['ACTIVE_DAYS'].max()), int(df['ACTIVE_DAYS'].median()))
input_active_quarters = st.sidebar.slider('Active Quarters', int(df['ACTIVE_QUARTERS'].min()), int(df['ACTIVE_QUARTERS'].max()), int(df['ACTIVE_QUARTERS'].median()))
input_avg_sessions_per_quarter = st.sidebar.slider('Avg Sessions Per Quarter', float(df['AVG_SESSIONS_PER_QUARTER'].min()), float(df['AVG_SESSIONS_PER_QUARTER'].max()), float(df['AVG_SESSIONS_PER_QUARTER'].median()))
input_avg_session_length_per_day = st.sidebar.slider('Avg Session Length Per Day', float(df['AVG_SESSION_LENGTH_PER_DAY'].min()), float(df['AVG_SESSION_LENGTH_PER_DAY'].max()), float(df['AVG_SESSION_LENGTH_PER_DAY'].median()))
input_age = st.sidebar.slider('Age', int(df['AGE'].min()), int(df['AGE'].max()), int(df['AGE'].median()))
input_tech_comfort_score = st.sidebar.slider('Tech Comfort Score', int(df['TECH_COMFORT_SCORE'].min()), int(df['TECH_COMFORT_SCORE'].max()), int(df['TECH_COMFORT_SCORE'].median()))

# Collect user input for categorical features
input_education = st.sidebar.selectbox('Education', options=df['EDUCATION'].unique())
input_income_level = st.sidebar.selectbox('Income Level', options=df['INCOME_LEVEL'].unique())
input_device_type = st.sidebar.selectbox('Device Type', options=df['DEVICE_TYPE'].unique())

# Create a DataFrame for the prediction
input_data = pd.DataFrame([{
    'TOTAL_SESSIONS': input_total_sessions,
    'GROSS_SESSION_LENGTH': input_gross_session_length,
    'ACTIVE_DAYS': input_active_days,
    'ACTIVE_QUARTERS': input_active_quarters,
    'AVG_SESSIONS_PER_QUARTER': input_avg_sessions_per_quarter,
    'AVG_SESSION_LENGTH_PER_DAY': input_avg_session_length_per_day,
    'AGE': input_age,
    'EDUCATION': input_education,
    'INCOME_LEVEL': input_income_level,
    'DEVICE_TYPE': input_device_type,
    'TECH_COMFORT_SCORE': input_tech_comfort_score
}])

# Ensure column order matches training data's X
input_data = input_data[X.columns]

# Make prediction
if st.sidebar.button('Predict Renewal') or 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = True
    prediction_proba = model_pipeline.predict_proba(input_data)[0]
    renewal_probability = prediction_proba[1]  # Probability of RENEWED=1
    churn_probability = prediction_proba[0]   # Probability of RENEWED=0

    st.subheader("Prediction Results:")
    st.metric(label="Renewal Probability", value=f"{renewal_probability:.2%}")
    st.metric(label="Churn Probability", value=f"{churn_probability:.2%}")

    if renewal_probability > 0.7:
        st.success("This customer is likely to renew!")
    elif renewal_probability < 0.3:
        st.warning("This customer is at high risk of churning.")
    else:
        st.info("Renewal probability is moderate. Further analysis may be needed.")

# --- Original Product Summary Dashboard ---
st.markdown("--- ")
st.subheader("Product Churn Summary (from initial request)")
# Data provided by the user, parsed into a DataFrame
data_summary = {
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

df_summary = pd.DataFrame(data_summary)
# Add Churn Score to the summary dataframe
df_summary['Churn Score'] = 1 - df_summary['Renewal Score']

st.sidebar.subheader("Product Summary Options")

# Sliders for Renewal Score range
renewal_score_min, renewal_score_max = st.sidebar.slider(
    "Filter by Renewal Score range:",
    min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.01,
    key='renewal_score_range_slider'
)

# Sliders for Churn Score range
churn_score_min, churn_score_max = st.sidebar.slider(
    "Filter by Churn Score range:",
    min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.01,
    key='churn_score_range_slider'
)

# Apply score filters
filtered_df_summary_scores = filtered_df_summary[
    (filtered_df_summary['Renewal Score'] >= renewal_score_min) &
    (filtered_df_summary['Renewal Score'] <= renewal_score_max) &
    (filtered_df_summary['Churn Score'] >= churn_score_min) &
    (filtered_df_summary['Churn Score'] <= churn_score_max)
]

display_score_type = st.sidebar.radio(
    "Display Score Type:",
    ('Renewal Score', 'Churn Score', 'Both'),
    index=0,
    key='display_score_type_radio'
)

# Filter by Primary Focus
selected_focus_summary = st.sidebar.multiselect(
    "Select Primary Focus (Product Summary):",
    options=df_summary["Primary Focus"].unique(),
    default=df_summary["Primary Focus"].unique(),
    key='summary_focus_multiselect'
)

# Re-apply focus filter after score filters
filtered_df_summary = filtered_df_summary_scores[filtered_df_summary_scores["Primary Focus"].isin(selected_focus_summary)]

# Sort by Score
sort_column_options = ['Renewal Score', 'Churn Score']
sort_by_summary = st.sidebar.radio(
    "Sort Product Summary by:",
    sort_column_options,
    index=0,
    key='summary_sort_radio'
)

sort_order_summary = st.sidebar.radio(
    "Sort Order (Product Summary):",
    ('High to Low', 'Low to High'),
    index=0,
    key='summary_sort_order_radio'
)

if sort_order_summary == 'High to Low':
    sorted_df_summary = filtered_df_summary.sort_values(by=sort_by_summary, ascending=False)
else:
    sorted_df_summary = filtered_df_summary.sort_values(by=sort_by_summary, ascending=True)

st.subheader("Product Churn Summary (Filtered and Sorted)")

if display_score_type == 'Renewal Score':
    st.dataframe(sorted_df_summary[['Product', 'Renewal Score', 'Primary Focus', 'Key Signal']])
elif display_score_type == 'Churn Score':
    st.dataframe(sorted_df_summary[['Product', 'Churn Score', 'Primary Focus', 'Key Signal']])
else: # Both
    st.dataframe(sorted_df_summary) # Will display all columns including both scores
