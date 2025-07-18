# --- Importing Libraries ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Import plotly.express
from sqlalchemy import create_engine, text 

# --- Database Connection Setup ---
# PostgreSQL DB connection
DATABASE_URL = "postgresql://rajuser:z3sEKFqYIAVVm65axXI5h1KGjMbEcznL@dpg-d18c1podl3ps73bun9k0-a.singapore-postgres.render.com/policestops"
engine = create_engine(DATABASE_URL)

# Function to run SQL queries
def run_query(query, params=None):
    with engine.connect() as conn:
        if params:
            return pd.read_sql(text(query), conn, params=params)
        else:
            return pd.read_sql(text(query), conn)

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide")

# Main Dashboard Title
st.markdown("""
<h1 style='color: #B22222; text-align: center; font-size: 70px; font-family: Verdana, Geneva, sans-serif; font-weight: 700;'>
🛑 Traffic Police Dashboard 🚓
</h1>
""", unsafe_allow_html=True)

# Header Images
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    st.image("C:/Users/KALAIRAJ/Downloads/stop1.png", use_container_width=True)
with col2:
    st.image("C:/Users/KALAIRAJ/Downloads/stop2.png", use_container_width=True)
with col3:
    st.image("C:/Users/KALAIRAJ/Downloads/stop3.png", use_container_width=True)

# --- Sidebar Navigation ---
menu = st.sidebar.selectbox("👇 Select to View", [
    "Vehicle Logs", "Violations", "Analytics & Trends"
])

# --- Main Content Sections based on Sidebar Selection ---

# 🔎 Vehicle Logs
if menu == "Vehicle Logs":
    st.header("🚦 Vehicle Logs")

    search = st.text_input("Search by Vehicle Number 🔎")
    if search:
        query = """
            SELECT * FROM police_stops
            WHERE vehicle_number ILIKE :search
            LIMIT 66000
        """
        params = {"search": f"%{search}%"}
    else:
        query = "SELECT * FROM police_stops LIMIT 66000"
        params = None
        
    try:
        df = run_query(query, params)
        st.dataframe(df)
    except Exception as e:
        st.error("Could not load vehicle logs.")
        st.code(str(e))

# 🚦 Violations
elif menu == "Violations":
    st.header("⚠️ Violations")

    query = """
        SELECT violation, COUNT(*) as count
        FROM police_stops
        GROUP BY violation
        ORDER BY count DESC
        LIMIT 100
    """
    params = None

    try:
        df = run_query(query, params)
        st.dataframe(df)
    except Exception as e:
        st.error("Could not load violations.")
        st.code(str(e))

# 📈 Analytics & Trends
if menu == "Analytics & Trends":
    st.header("📊 High-Risk Vehicles and Trends")

    tab1, tab2 = st.tabs(["Stops by Violation", "Driver Gender Distribution"])

    query_for_tabs = """
    SELECT violation, driver_gender
    FROM police_stops
    LIMIT 100
    """
    data = run_query(query_for_tabs)
    with tab1:                               #Tab 1: Stops by Violation
        if not data.empty and 'violation' in data.columns:
            violation_data = data['violation'].value_counts().reset_index()
            fig = px.bar(violation_data, x='violation', y='count', title='Stop by Violation Type', color='violation')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for violation chart.")

    with tab2:                               #Tab 2: Driver Gender Distribution
        if not data.empty and 'driver_gender' in data.columns:
            gender_data = data['driver_gender'].value_counts().reset_index()
            gender_data.columns = ['Gender', 'Count']
            fig = px.bar(gender_data, x='Gender', y='Count', title="Driver Gender Distribution", color='Gender')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for Driver Gender chart.")

# --- Enforcement Overview Metrics ---
st.markdown("### 📊 <span style='color:#1E90FF;'>Enforcement Overview</span>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# Helper function to get single scalar results from DB
def get_scalar(query, params=None):
    with engine.connect() as conn:
        if params:
            return conn.execute(text(query), params).scalar()
        else:
            return conn.execute(text(query)).scalar()

try:
    total_stops = get_scalar("SELECT COUNT(*) FROM police_stops")
    total_arrests = get_scalar("SELECT COUNT(*) FROM police_stops WHERE stop_outcome ILIKE :arrest", {"arrest": "%arrest%"})
    total_warnings = get_scalar("SELECT COUNT(*) FROM police_stops WHERE stop_outcome ILIKE :warning", {"warning": "%warning%"})
    drug_related = get_scalar("SELECT COUNT(*) FROM police_stops WHERE drugs_related_stop = TRUE")

    col1.metric("🚦Total Police Stops", f"{total_stops}")
    col2.metric("🚓Total Arrests", f"{total_arrests}")
    col3.metric("⚠️Total Warnings", f"{total_warnings}")
    col4.metric("💊Drug Related Stops", f"{drug_related}")

except Exception as e:
    st.error("Error fetching key metrics.")
    st.code(str(e))

# --- Traffic Intelligence Section (Simple Queries) ---
st.markdown("### 💡 <span style='color: #1E90FF;'>Traffic Intelligence</span>", unsafe_allow_html=True)

selected_query = st.selectbox("Select a Query to Run", [
    "Total Number of Police Stops",
    "Count of Stops by Violation Type",
    "Number of Arrests vs Warnings",
    "Average Age of Drivers Stopped",
    "Top 5 Most Frequent Search Types",
    "Count of Stops by Gender",
    "Most Common Violation for Arrests"
])

query_map = {
    "Total Number of Police Stops": "SELECT COUNT(*) AS total_stops FROM police_stops",
    "Count of Stops by Violation Type": "SELECT violation, COUNT(*) AS count FROM police_stops GROUP BY violation ORDER BY count DESC",
    "Number of Arrests vs Warnings": "SELECT stop_outcome, COUNT(*) AS count FROM police_stops GROUP BY stop_outcome",
    "Average Age of Drivers Stopped": "SELECT AVG(driver_age) AS average_age FROM police_stops",
    "Top 5 Most Frequent Search Types": "SELECT search_type, COUNT(*) FROM police_stops WHERE search_type != '' GROUP BY search_type ORDER BY COUNT(*) DESC LIMIT 5",
    "Count of Stops by Gender": "SELECT driver_gender, COUNT(*) AS count FROM police_stops GROUP BY driver_gender",
    "Most Common Violation for Arrests": "SELECT violation, COUNT(*) AS count FROM police_stops WHERE stop_outcome LIKE '%arrest%' GROUP BY violation ORDER BY count DESC LIMIT 10"
}

if st.button("Search"):
    try:
        result = run_query(query_map[selected_query])
        st.dataframe(result) 
    except Exception as e:
        st.error(f"Query Error: {e}")

# --- Add New Police Log and Predict Section ---
st.subheader("➕ Add New Police Log & Predict 📋")
st.markdown("Fill in the details below to get a natural language prediction of the stop outcome based on existing data.")

with st.form("new_log"):
    col1, col2 = st.columns(2)
    with col1:
        stop_date = st.date_input("Stop Date")
        stop_time = st.text_input("Stop Time (HH:MM)")
        country = st.text_input("Country Name")
        driver_name = st.text_input("Driver Name")
        gender = st.selectbox("Driver Gender", ["Male", "Female", "Other"])
        age = st.number_input("Driver Age", min_value=16, max_value=100, step=1)
    with col2:
        race = st.text_input("Driver Race")
        search = st.selectbox("Was a Search Conducted?", ["Yes", "No"])
        search_type = st.text_input("Search Type")
        drug_related = st.selectbox("Was it Drug Related?", ["Yes", "No"])
        duration = st.text_input("Stop Duration")
        vehicle = st.text_input("Vehicle Number")

    submit = st.form_submit_button("Predict Stop Outcome & Violation")

    if submit:
        predicted_violation = "Speeding"  
        predicted_outcome = "Citation"    

        # Convert to boolean-like values
        search_conducted = 1 if search == "Yes" else 0
        drugs_related_stop = 1 if drug_related == "Yes" else 0

        # Natural language summary
        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

        st.markdown(f"""
        ## 🧾 **Prediction Summary**

        - **Predicted Violation:** `{predicted_violation}`
        - **Predicted Stop Outcome:** `{predicted_outcome}`

        📋 A {int(age)}-year-old {gender} driver in `{country}` was stopped at `{stop_time}` on `{stop_date}`. 
        {search_text}, and the stop {drug_text}. 
        Stop duration: `{duration}` 
        Vehicle Number: **{vehicle}**
        """)

# --- SQL Queries (Advanced Analysis) ---
st.markdown("### 🛑 <span style='color:#2196F3;'>Police Stop Query</span>", unsafe_allow_html=True)
selected_query = st.selectbox("Select Analysis", [
    "Top 10 Vehicles in Drug Stops",
    "Most Frequently Searched Vehicles",
    "Driver Age Group with Highest Arrest Rate",
    "Gender Distribution by Country",
    "Race + Gender with Highest Search Rate",
    "Time of Day with Most Stops",
    "Average Stop Duration by Violation",
    "Are Night Stops More Likely to be Arrests?",
    "Violations Linked with Search or Arrest",
    "Violations Common Among <25",
    "Violations Rarely Leading to Search or Arrest",
    "Countries with Highest Drug Stop Rate",
    "Arrest Rate by Country & Violation",
    "Country with Most Searches Conducted"
])

query_map = {
    "Top 10 Vehicles in Drug Stops": "SELECT vehicle_number, COUNT(*) AS stop_count FROM police_stops WHERE drugs_related_stop = TRUE GROUP BY vehicle_number ORDER BY stop_count DESC LIMIT 10;",
    "Most Frequently Searched Vehicles": "SELECT vehicle_number, COUNT(*) AS search_count FROM police_stops WHERE search_conducted = TRUE GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10;",
    "Driver Age Group with Highest Arrest Rate": "SELECT CASE WHEN driver_age < 18 THEN '<18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 40 THEN '26-40' WHEN driver_age BETWEEN 41 AND 60 THEN '41-60' ELSE '60+' END AS age_group, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate FROM police_stops GROUP BY age_group ORDER BY arrest_rate DESC;",
    "Gender Distribution by Country": "SELECT country_name, driver_gender, COUNT(*) AS total_stops FROM police_stops GROUP BY country_name, driver_gender ORDER BY country_name;",
    "Race + Gender with Highest Search Rate": "SELECT driver_race, driver_gender, COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate FROM police_stops GROUP BY driver_race, driver_gender ORDER BY search_rate DESC LIMIT 1;",
    "Time of Day with Most Stops": "SELECT CASE WHEN EXTRACT(HOUR FROM stop_time::time) BETWEEN 0 AND 5 THEN 'Night (12AM-6AM)' WHEN EXTRACT(HOUR FROM stop_time::time) BETWEEN 6 AND 11 THEN 'Morning (6AM-12PM)' WHEN EXTRACT(HOUR FROM stop_time::time) BETWEEN 12 AND 17 THEN 'Afternoon (12PM-6PM)' ELSE 'Evening (6PM-12AM)' END AS time_of_day, COUNT(*) AS stop_count FROM police_stops GROUP BY time_of_day ORDER BY stop_count DESC;",
    "Average Stop Duration by Violation": "SELECT violation, AVG(CASE WHEN stop_duration ILIKE '%0-15%' THEN 7.5 WHEN stop_duration ILIKE '%16-30%' THEN 23 WHEN stop_duration ILIKE '%30+%' THEN 45 ELSE NULL END) AS avg_duration_minutes FROM police_stops GROUP BY violation ORDER BY avg_duration_minutes DESC;",
    "Are Night Stops More Likely to be Arrests?": "SELECT CASE WHEN EXTRACT(HOUR FROM stop_time::time) BETWEEN 0 AND 5 THEN 'Night' ELSE 'Day' END AS period, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate FROM police_stops GROUP BY period;",
    "Violations Linked with Search or Arrest": "SELECT violation, COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%') AS related_events, COUNT(*) AS total_stops, ROUND((COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%')::numeric / COUNT(*)::numeric) * 100, 2) AS rate_percent FROM police_stops GROUP BY violation ORDER BY rate_percent DESC;",
    "Violations Common Among <25": "SELECT violation, COUNT(*) AS total FROM police_stops WHERE driver_age < 25 GROUP BY violation ORDER BY total DESC;",
    "Violations Rarely Leading to Search or Arrest": "SELECT violation, COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%') AS related_events, COUNT(*) AS total_stops, ROUND((COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%')::numeric / COUNT(*)::numeric) * 100, 2) AS rate_percent FROM police_stops GROUP BY violation HAVING COUNT(*) > 5 ORDER BY rate_percent ASC LIMIT 5;",
    "Countries with Highest Drug Stop Rate": "SELECT country_name, COUNT(*) FILTER (WHERE drugs_related_stop = TRUE)::float / COUNT(*) AS drug_rate FROM police_stops GROUP BY country_name ORDER BY drug_rate DESC;",
    "Arrest Rate by Country & Violation": "SELECT country_name, violation, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate FROM police_stops GROUP BY country_name, violation ORDER BY arrest_rate DESC;",
    "Country with Most Searches Conducted": "SELECT country_name, COUNT(*) AS search_count FROM police_stops WHERE search_conducted = TRUE GROUP BY country_name ORDER BY search_count DESC LIMIT 1;"
}

if st.button("Run Query"): 
    result = run_query(query_map[selected_query])
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("No results found.")

# --- Advanced Police Stop Analysis (More Complex Queries) ---
st.markdown("### 🚔 <span style='color:#2196F3;'>Advanced Police Stop Analysis</span>", unsafe_allow_html=True)
selected_query = st.selectbox("Select Analysis", [
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops",
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country",
    "Top 5 Violations with Highest Arrest Rates"
])

query_map = {
    "Yearly Breakdown of Stops and Arrests by Country": "SELECT country_name, EXTRACT(YEAR FROM stop_date::DATE) AS year, COUNT(*) AS total_stops, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS total_arrests, ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate_percent, RANK() OVER (PARTITION BY EXTRACT(YEAR FROM stop_date::DATE) ORDER BY COUNT(*) DESC) AS country_rank FROM police_stops WHERE stop_date IS NOT NULL GROUP BY country_name, year ORDER BY year, country_rank;",
    "Driver Violation Trends Based on Age and Race": "SELECT v.driver_age, v.driver_race, v.violation, COUNT(*) AS count FROM (SELECT driver_age, driver_race, violation FROM police_stops WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL) v GROUP BY v.driver_age, v.driver_race, v.violation ORDER BY count DESC LIMIT 100;",
    "Time Period Analysis of Stops": "SELECT EXTRACT(YEAR FROM stop_date::date) AS year, TO_CHAR(stop_date::date, 'Month') AS month, DATE_PART('hour', stop_time::time) AS hour, COUNT(*) AS stop_count FROM police_stops GROUP BY year, month, hour ORDER BY year, month, hour;",
    "Violations with High Search and Arrest Rates": "SELECT violation, COUNT(*) AS total_stops, COUNT(*) FILTER (WHERE search_conducted = TRUE) AS total_searches, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS total_arrests, ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = TRUE) / COUNT(*), 2) AS search_rate, ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate, RANK() OVER (ORDER BY COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') DESC) AS arrest_rank FROM police_stops GROUP BY violation ORDER BY arrest_rate DESC LIMIT 10;",   
    "Driver Demographics by Country": "SELECT country_name, driver_gender, driver_race, ROUND(AVG(driver_age), 1) AS avg_age, COUNT(*) AS driver_count FROM police_stops WHERE driver_age IS NOT NULL GROUP BY country_name, driver_gender, driver_race ORDER BY country_name, driver_count DESC;",    
    "Top 5 Violations with Highest Arrest Rates": "SELECT violation, COUNT(*) AS total_stops, COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS arrest_count, ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate FROM police_stops GROUP BY violation HAVING COUNT(*) > 10 ORDER BY arrest_rate DESC LIMIT 5;"
}

if st.button("Run Analysis"): 
    result = run_query(query_map[selected_query])
    if not result.empty:
        st.dataframe(result)
    else:
         st.warning("No results found.")



# --- Overall Flow and Purpose: ---
# 1. Setup: Connects to a PostgreSQL database and defines a utility function for running queries.
# 2. Dashboard Layout: Configures the Streamlit page, adds a title, and displays header images.
# 3. Navigation: Uses a sidebar selectbox to allow users to switch between different dashboard views.
# 4. Vehicle Logs: Provides a searchable table of police stop records.
# 5. Violations: Shows a table of the most common violation types.
# 6. Analytics & Trends: Presents interactive charts (bar charts for violations and gender distribution) to visualize key trends.
# 7. Enforcement Overview: Displays key performance indicators (KPIs) like total stops, arrests, warnings, and drug-related stops using metric cards.
# 8. Traffic Intelligence (Simple Queries): Allows users to run predefined basic SQL queries to get quick insights.
# 9. Add New Police Log & Predict: Offers a form for users to input new police stop details. Crucially, this section is set up to simulate a prediction, implying that an ML model would be integrated here to predict stop outcomes and violations based on the input data.
# 10. Police Stop Query (Advanced Analysis): Provides a selection of more complex SQL queries for deeper, pre-defined analytical investigations (e.g., age group with highest arrest rate, time of day with most stops).
# 11. Advanced Police Stop Analysis (More Complex Queries): Offers even more sophisticated analytical queries, often involving more complex SQL features, for in-depth data exploration.

# This script demonstrates a comprehensive Streamlit dashboard for a traffic police department, enabling data exploration, quick insights, and a framework for integrating predictive analytics.

# Streamlit App Architecture Overview
#
# +-------------------------+
# |   Streamlit App Launch  |
# +-------------------------+
#             |
#             v
# +--------------------------+
# | Connect to PostgreSQL DB |
# +--------------------------+
#             |
#             v
# +--------------------------+
# |   Sidebar Menu Selection |
# +--------------------------+
#      |       |       |
#      v       v       v
# Vehicle  Violations Analytics
#  Logs        & Trends
#   |             |
#   v             v
# Search or   Charts & Metrics
# Full View     via Plotly
#   |             |
#   v             v
# +--------------------------+
# |   SQL Queries Executed   |
# +--------------------------+
#             |
#             v
# +--------------------------+
# | Results Displayed on UI  |
# +--------------------------+