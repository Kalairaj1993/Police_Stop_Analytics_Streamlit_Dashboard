# 🚓 Police Stop Data Analytics Dashboard

A real-time, SQL-powered data analytics dashboard for police check post management using **Python**, **PostgreSQL**, and **Streamlit**.

---

## 👋 Introduction

Hi, I'm excited to present the workflow of my data analytics project, focusing on **police stop data**. This project leverages the power of **Python** and a robust **PostgreSQL database hosted on Visual Studio** to provide insightful analytics and trends.

Let’s walk through the key phases of my development process:

---

## 🔧 Project Workflow

### 🧱 Phase 1: Establishing PostgreSQL on Visual Studio

**Objective**: To set up the database instance and secure all necessary connection details.

**Process**:
- I created a new PostgreSQL database on **Visual Studio**.
- Extracted the connection string, host, port, database name, username, and password.
- These credentials were essential for connecting my local development environment to the remote PostgreSQL database hosted on Visual Studio.

---

### 💻 Phase 2: Preparing My Development Arena – Visual Studio Code

**Objective**: To establish a clean and efficient Python development workspace.

**Process**:
- I created a dedicated project directory named `police_stops`.
- Set up a Python virtual environment inside the directory.
- Installed essential libraries:
  - `psycopg2-binary` for PostgreSQL connectivity
  - `pandas` for powerful data manipulation

---

### 🔌 Phase 3: My Python Database Connector (`police.py`)

**Objective**: To programmatically connect my Python application to the Visual Studio-hosted PostgreSQL database.

**Process**:
- Implemented connection logic using `psycopg2` in `police.py`.
- Used **Render** connection URL and environment variables to securely manage credentials.
- Created the `run_query()` function to fetch and execute SQL queries seamlessly.

---

### 📥 Phase 4: Ingesting and Structuring My Data

**Objective**: To load raw police stop data into a pandas DataFrame for analysis.

**Process**:
- Used `run_query()` to fetch columns such as `violation`, `driver_gender`, `stop_date`, and `stop_time`.
- These formed the base DataFrame for downstream analytics.

---

### 🧹 Phase 5: Refining the Raw – Data Cleaning and Preprocessing

**Objective**: To transform raw data into a clean, consistent, and analysis-ready state.

**Process**:
- **Date and Time Handling**: Combined `stop_date` and `stop_time` into a unified `stop_datetime` object.
- **Null Handling**:
  - Filled missing `violation` entries with `'Unknown'`
  - Removed rows with missing `driver_gender`
- **Further Refinement**: Removed duplicates and standardized text formats where needed.

---

### 📊 Phase 6: Unveiling Insights – Analytics & Visualization

**Objective**: To build interactive visualizations and dashboards using cleaned data.

**Process**:
- Used `plotly.express` for dynamic visualizations.
- Integrated visuals into Streamlit via `st.plotly_chart()`.
- Dashboard provides trends, demographic insights, and vehicle stop analytics in real-time.

---

## 📌 Problem Statement

Police check posts require a centralized system for logging, tracking, and analyzing vehicle movements. Current systems are manual and inefficient.

> This project builds an **SQL-based check post database** and a **Streamlit dashboard** for real-time insights and alerts.

---

## 💼 Business Use Cases

- ✅ Real-time logging of vehicles and personnel
- 🚨 Automated suspect vehicle identification using SQL
- 📈 Efficiency monitoring of check post operations
- 🔁 Crime pattern analysis using Python
- 🌐 Centralized database for multi-location posts

---

## 🛠️ Technical Approach

### Step 1: Python for Data Processing
- Removed columns with all missing values
- Cleaned null values and formatted date/time

### Step 2: Database Design (PostgreSQL)
- Designed SQL schema and created necessary tables
- Inserted police stop records into PostgreSQL

### Step 3: Streamlit Dashboard
- Visualize vehicle logs, violations, and personnel reports
- Implement SQL-based filters for search
- Generate trend analysis (e.g., high-risk vehicles)

---

## 📈 SQL Queries

### 🚗 Vehicle-Based
- Top 10 vehicles in drug-related stops
- Most frequently searched vehicles

### 🧍 Demographic-Based
- Gender distribution by country
- Arrest rate by age group
- Highest search rate by race and gender

### 🕒 Time & Duration-Based
- Peak hours for stops
- Average stop duration per violation
- Arrest likelihood during night stops

### ⚖ Violation-Based
- Violations linked to arrests/searches
- Violations by drivers < 25 years
- Rarely searched/arrested violations

### 🌍 Location-Based
- Countries with high drug stop rates
- Arrest rate by country and violation
- Most stops with searches per country

### 🧠 Complex Analysis
- Yearly breakdown by country using window functions
- Violation trends by age & race (joins)
- Time-period analysis using date functions
- Top 5 violations with highest arrest rates

---

## ✅ Results

| Outcome                      | Description                                     |
|------------------------------|-------------------------------------------------|
| 🚀 Faster Operations         | Real-time performance through optimized queries |
| 🔔 Automated Alerts          | Flag suspect vehicles instantly                 |
| 📊 Visual Reporting          | Live insights for officers                      |
| 📉 Data-Driven Decisions     | Smarter enforcement with trend analysis         |

---

## 📏 Project Evaluation Metrics

| Metric                  | Purpose                                              |
|-------------------------|------------------------------------------------------|
| ⏱️ Query Execution Time  | Optimize SQL for real-time analysis                 |
| ✅ Data Accuracy         | Ensure all entries are correct & consistent         |
| 📶 System Uptime         | Support uninterrupted updates                       |
| 👮 User Engagement       | Measure system usage by officers                    |
| 🚓 Violation Detection   | Monitor flagged vehicle identification rate         |

---

## 💻 Tech Stack

- **Language**: Python
- **Database**: PostgreSQL (hosted on Visual Studio)
- **Frameworks**: Streamlit, pandas, plotly
- **Connector**: psycopg2-binary
- **IDE**: Visual Studio Code

---
## 🗂️ Project Structure – Police Stop Data Analytics Dashboard

| File/Folder                | Purpose                                                                 |
|----------------------------------|-------------------------------------------------------------------------|
| `police_stops/`           | Root directory of the project                                           |
| ├── `.venv/`              | Python virtual environment (created using Visual Studio Code)           |
| ├── `data/`               | Folder for local raw data files (e.g., CSVs)                            |
| │     └── `raw_police_stops.csv` | Raw police stop data used for ingestion                           |
| ├── `police.py`           | Python script to connect with PostgreSQL and ingest/query data          |
| ├── `streamlit_app.py`    | Main Streamlit dashboard application with visualizations                |
| ├── `requirements.txt`    | Python dependencies (e.g., pandas, psycopg2-binary, plotly, streamlit) |
| └── `README.md`           | Project documentation (this file)                                       |

### 🔗 Development Tools & Environment

- **IDE**: Visual Studio Code  
- **Database**: PostgreSQL hosted via Visual Studio  
- **Language**: Python  
- **Libraries**: `pandas`, `psycopg2-binary`, `plotly`, `streamlit`  
- **Visualization**: Real-time dashboard using `plotly.express` in Streamlit  
- **Hosting**: PostgreSQL instance managed and connected through Render or Visual Studio

