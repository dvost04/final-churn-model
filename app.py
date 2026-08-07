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
elif sort_order == 'Low to High':
    sorted_df = filtered_df.sort_values(by="Renewal Score", ascending=True)

st.subheader("Filtered and Sorted Results")
st.dataframe(sorted_df)

deployment_instructions = """
---
### How to Deploy this Application to Render

To deploy this interactive dashboard on Render with a live URL, you'll need to prepare several files and push them to a GitHub repository. Follow these steps:

1.  **Save this code as `app.py`:**
    Copy the entire Python code above (from `import streamlit as st` down to this markdown block) and save it as a file named `app.py` on your local machine.

2.  **Create `requirements.txt`:**
    Create a file named `requirements.txt` in the same directory as `app.py` with the following content:
    ```
    streamlit
    pandas
    ```

3.  **Create `Procfile` (for Render):**
    Create a file named `Procfile` (no extension) in the same directory as `app.py` with the following content:
    ```
    web: sh setup.sh && streamlit run app.py --server.port $PORT --server.enableCORS false
    ```

4.  **Create `setup.sh` (for Render):**
    Create a file named `setup.sh` in the same directory as `app.py` with the following content:
    ```bash
    set -e
    mkdir -p "$HOME/.streamlit"
    echo "[server]\nheadless = true\nenableCORS = false\nport = $PORT" > "$HOME/.streamlit/config.toml"
    ```
    *Note 1: Render often requires Streamlit to be configured to run on the assigned port and disables Cross-Origin Resource Sharing (CORS) for security/deployment ease.* This updated script is more robust for Render environments.
    *Note 2: **CRITICAL:** Ensure this `setup.sh` file uses **Unix-style line endings (LF)**, not Windows-style (CRLF). If you edit it on Windows, you may need to explicitly save it with LF line endings in your text editor to avoid `Illegal option -` errors during deployment.

5.  **Initialize a Git repository and push to GitHub:**
    *   Open your terminal or command prompt.
    *   Navigate to the directory containing `app.py`, `requirements.txt`, `Procfile`, and `setup.sh`.
    *   Initialize a Git repository:
        ```bash
        git init
        ```
    *   Add your files:
        ```bash
        git add .
        ```
    *   Commit your changes:
        ```bash
        git commit -m \"Initial Streamlit churn dashboard\"
        ```
    *   Create a new **public** repository on GitHub (e.g., `my-churn-dashboard`).
    *   Link your local repository to the GitHub one (replace `<YOUR_GITHUB_REPO_URL>` with your actual repo URL):
        ```bash
        git remote add origin <YOUR_GITHUB_REPO_URL>
        git branch -M main
        git push -u origin main
        ```

6.  **Deploy on Render.com:**
    *   Go to [Render.com](https://render.com/) and log in.
    *   Click on \"New\" -> \"Web Service\".
    *   Connect your GitHub account and select the repository you just pushed (e.g., `my-churn-dashboard`).
    *   Render will automatically detect `requirements.txt` and `Procfile`.
    *   **Environment:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `sh setup.sh && streamlit run app.py --server.port $PORT --server.enableCORS false`
    *   Choose a region (e.g., \"Oregon\").
    *   Click \"Create Web Service\".

Render will then build and deploy your application. Once deployed, you will get a live URL that you can share.
"""

st.markdown(deployment_instructions)
