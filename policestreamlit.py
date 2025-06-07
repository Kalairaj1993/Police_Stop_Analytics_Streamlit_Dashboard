import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

# PostgreSQL DB connection
DATABASE_URL = "postgresql://rajuser:Miezb4Wu9cf3VZ30YCBedzlyYW1hzmFm@dpg-d0ka3bruibrs739bsct0-a.singapore-postgres.render.com/police"
engine = create_engine(DATABASE_URL)

def run_query(query, params=None):
    with engine.connect() as conn:
        if params:
            return pd.read_sql(text(query), conn, params=params)
        else:
            return pd.read_sql(text(query), conn)

st.set_page_config(layout="wide")

st.markdown("""
<h1 style='color: #FF4B4B; text-align: center;'>🛑 Traffic Police Dashboard 🚓</h1>
""", unsafe_allow_html=True)

# Sidebar menu
menu = st.sidebar.selectbox("👇 Select to View", [
"Vehicle Logs", "Violations", "Analytics & Trends"
])

# 🔎 Vehicle Logs
if menu == "Vehicle Logs":
    st.header("🚦 Vehicle Logs")
    # ...

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

elif menu == "Analytics & Trends":
    st.header("📊 High-Risk Vehicles and Trends")

    query = """
        SELECT violation, COUNT(*) AS count
        FROM police_stops
        GROUP BY violation
        ORDER BY count DESC
    """
    try:
        df = run_query(query)
        st.subheader("🚨 Most Common Violations")
        st.bar_chart(df.set_index("violation"))
    except Exception as e:
        st.error("Failed to load analytics.")
        st.code(str(e))

### Enforcement Overview
st.markdown("### 📊 <span style='color:#1E90FF;'>Enforcement Overview</span>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

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

# --- Traffic Intelligence ---
st.markdown("### 💡 <span style='color: #1E90FF;'>Traffic Intelligence</span>", unsafe_allow_html=True)

selected_query = st.selectbox("Select a Query to Run", [
    "Total Number of Police Stops",
    "Count of Stops by Violation Type",
    "Number of Arrests vs. Warnings",
    "Average Age of Drivers Stopped",
    "Top 5 Most Frequent Search Types",
    "Count of Stops by Gender",
    "Most Common Violation for Arrests"
])

query_map = {
    "Total Number of Police Stops": "SELECT COUNT(*) AS total_stops FROM police_stops",
    "Count of Stops by Violation Type": "SELECT violation, COUNT(*) AS count FROM police_stops GROUP BY violation ORDER BY count DESC",
    "Number of Arrests vs. Warnings": "SELECT stop_outcome, COUNT(*) AS count FROM police_stops GROUP BY stop_outcome",
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

# --- Add New Police Log and Predict ---
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
        # Placeholder for predicted results from ML model
        predicted_violation = "Speeding"  # Replace with model.predict(...)
        predicted_outcome = "Citation"    # Replace with model.predict(...)

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

#####SQL QUERIES#####
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
    "Top 10 Vehicles in Drug Stops": """
        SELECT vehicle_number, COUNT(*) AS stop_count
        FROM police_stops
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY stop_count DESC
        LIMIT 10;
    """,

    "Most Frequently Searched Vehicles": """
        SELECT vehicle_number, COUNT(*) AS search_count
        FROM police_stops
        WHERE search_conducted = TRUE
        GROUP BY vehicle_number
        ORDER BY search_count DESC
        LIMIT 10;
    """,

    "Driver Age Group with Highest Arrest Rate": """
        SELECT 
            CASE 
                WHEN driver_age < 18 THEN '<18'
                WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                ELSE '60+' 
            END AS age_group,
            COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate
        FROM police_stops
        GROUP BY age_group
        ORDER BY arrest_rate DESC;
    """,

    "Gender Distribution by Country": """
        SELECT country_name, driver_gender, COUNT(*) AS total_stops
        FROM police_stops
        GROUP BY country_name, driver_gender
        ORDER BY country_name;
    """,

    "Race + Gender with Highest Search Rate": """
        SELECT driver_race, driver_gender, 
               COUNT(*) FILTER (WHERE search_conducted = TRUE)::float / COUNT(*) AS search_rate
        FROM police_stops
        GROUP BY driver_race, driver_gender
        ORDER BY search_rate DESC
        LIMIT 1;
    """,

    "Time of Day with Most Stops": """
        SELECT 
            CASE 
                WHEN EXTRACT(HOUR FROM stop_time)::int BETWEEN 0 AND 5 THEN 'Night (12AM-6AM)'
                WHEN EXTRACT(HOUR FROM stop_time)::int BETWEEN 6 AND 11 THEN 'Morning (6AM-12PM)'
                WHEN EXTRACT(HOUR FROM stop_time)::int BETWEEN 12 AND 17 THEN 'Afternoon (12PM-6PM)'
                ELSE 'Evening (6PM-12AM)'
            END AS time_of_day,
            COUNT(*) AS stop_count
        FROM police_stops
        GROUP BY time_of_day
        ORDER BY stop_count DESC;
    """,

    "Average Stop Duration by Violation": """
        SELECT violation, AVG(
            CASE
                WHEN stop_duration ILIKE '%0-15%' THEN 7.5
                WHEN stop_duration ILIKE '%16-30%' THEN 23
                WHEN stop_duration ILIKE '%30+%' THEN 45
                ELSE NULL
            END
        ) AS avg_duration_minutes
        FROM police_stops
        GROUP BY violation
        ORDER BY avg_duration_minutes DESC;
    """,

    "Are Night Stops More Likely to be Arrests?": """
        SELECT 
            CASE 
                WHEN EXTRACT(HOUR FROM stop_time)::int BETWEEN 0 AND 5 THEN 'Night'
                ELSE 'Day'
            END AS period,
            COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate
        FROM police_stops
        GROUP BY period;
    """,

    "Violations Linked with Search or Arrest": """
        SELECT violation,
               COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%') AS related_events,
               COUNT(*) AS total_stops,
               ROUND(COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%')::float / COUNT(*) * 100, 2) AS rate_percent
        FROM police_stops
        GROUP BY violation
        ORDER BY rate_percent DESC;
    """,

    "Violations Common Among <25": """
        SELECT violation, COUNT(*) AS total
        FROM police_stops
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY total DESC;
    """,

    "Violations Rarely Leading to Search or Arrest": """
        SELECT violation,
               COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%') AS related_events,
               COUNT(*) AS total_stops,
               ROUND(COUNT(*) FILTER (WHERE search_conducted = TRUE OR stop_outcome ILIKE '%arrest%')::float / COUNT(*) * 100, 2) AS rate_percent
        FROM police_stops
        GROUP BY violation
        HAVING COUNT(*) > 5
        ORDER BY rate_percent ASC
        LIMIT 5;
    """,

    "Countries with Highest Drug Stop Rate": """
        SELECT country_name,
               COUNT(*) FILTER (WHERE drugs_related_stop = TRUE)::float / COUNT(*) AS drug_rate
        FROM police_stops
        GROUP BY country_name
        ORDER BY drug_rate DESC;
    """,

    "Arrest Rate by Country & Violation": """
        SELECT country_name, violation,
               COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%')::float / COUNT(*) AS arrest_rate
        FROM police_stops
        GROUP BY country_name, violation
        ORDER BY arrest_rate DESC;
    """,

    "Country with Most Searches Conducted": """
        SELECT country_name, COUNT(*) AS search_count
        FROM police_stops
        WHERE search_conducted = TRUE
        GROUP BY country_name
        ORDER BY search_count DESC
        LIMIT 1;
    """
}

if st.button("Run Query"):
    try:
        result = run_query(query_map[selected_query])
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Query Error: {e}")

####(Complex)####
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
    "Yearly Breakdown of Stops and Arrests by Country": """
        SELECT 
            country_name,
            EXTRACT(YEAR FROM stop_date) AS year,
            COUNT(*) AS total_stops,
            COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS total_arrests,
            ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate_percent,
            RANK() OVER (PARTITION BY EXTRACT(YEAR FROM stop_date) ORDER BY COUNT(*) DESC) AS country_rank
        FROM police_stops
        GROUP BY country_name, year
        ORDER BY year, country_rank;
    """,

    "Driver Violation Trends Based on Age and Race": """
        SELECT 
            v.driver_age,
            v.driver_race,
            v.violation,
            COUNT(*) AS count
        FROM (
            SELECT driver_age, driver_race, violation
            FROM police_stops
            WHERE driver_age IS NOT NULL AND driver_race IS NOT NULL
        ) v
        GROUP BY v.driver_age, v.driver_race, v.violation
        ORDER BY count DESC
        LIMIT 100;
    """,

    "Time Period Analysis of Stops": """
        SELECT 
            EXTRACT(YEAR FROM stop_date) AS year,
            TO_CHAR(stop_date, 'Month') AS month,
            DATE_PART('hour', stop_time) AS hour,
            COUNT(*) AS stop_count
        FROM police_stops
        GROUP BY year, month, hour
        ORDER BY year, month, hour;
    """,

    "Violations with High Search and Arrest Rates": """
        SELECT 
            violation,
            COUNT(*) AS total_stops,
            COUNT(*) FILTER (WHERE search_conducted = TRUE) AS total_searches,
            COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS total_arrests,
            ROUND(100.0 * COUNT(*) FILTER (WHERE search_conducted = TRUE) / COUNT(*), 2) AS search_rate,
            ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate,
            RANK() OVER (ORDER BY COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') DESC) AS arrest_rank
        FROM police_stops
        GROUP BY violation
        ORDER BY arrest_rate DESC
        LIMIT 10;
    """,

    "Driver Demographics by Country": """
        SELECT 
            country_name,
            driver_gender,
            driver_race,
            ROUND(AVG(driver_age), 1) AS avg_age,
            COUNT(*) AS driver_count
        FROM police_stops
        WHERE driver_age IS NOT NULL
        GROUP BY country_name, driver_gender, driver_race
        ORDER BY country_name, driver_count DESC;
    """,

    "Top 5 Violations with Highest Arrest Rates": """
        SELECT 
            violation,
            COUNT(*) AS total_stops,
            COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') AS arrest_count,
            ROUND(100.0 * COUNT(*) FILTER (WHERE stop_outcome ILIKE '%arrest%') / COUNT(*), 2) AS arrest_rate
        FROM police_stops
        GROUP BY violation
        HAVING COUNT(*) > 10
        ORDER BY arrest_rate DESC
        LIMIT 5;
    """
}

if st.button("Run Analysis"):
    try:
        result = run_query(query_map[selected_query])
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Query Error: {e}")






