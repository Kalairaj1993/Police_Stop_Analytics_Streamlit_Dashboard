# 🚓 Police Stop Data Analytics Dashboard

A real-time, SQL-powered data analytics dashboard for managing police check post operations using **Python**, **pandas**, **Streamlit**, and a **PostgreSQL database hosted on Render.com**. Developed in **Visual Studio Code**.

---

## 📌 Overview

This project analyzes and visualizes police stop data to provide insights into violations, arrest trends, stop times, and demographic patterns. It integrates a cloud-hosted PostgreSQL database and an interactive Streamlit dashboard.

Let’s walk through the key phases of my development process:

---

## ⚙️ Features

- 📊 Interactive Streamlit dashboard for police data insights
- 🚨 Real-time analysis of stops, arrests, and violations
- 🔍 SQL queries for demographic and time-based analytics
- 🧹 Data cleaning and transformation using `pandas`
- ☁️ Cloud-hosted PostgreSQL on Render.com

---

## 🧠 What I Did

- ✅ Connected to a **PostgreSQL** database hosted on **Render.com**
- 🔐 Managed credentials securely via environment variables
- 🧼 Cleaned and transformed raw police stop data using **pandas**
- 📈 Built an interactive dashboard using **Streamlit** and **plotly**
- 🧑‍💻 Developed and tested the full project in **Visual Studio Code**

---

## 🔧 Project Workflow

### 🧱 Phase 1: Establishing PostgreSQL on Render.com

**Objective**: Set up a cloud-hosted PostgreSQL database and retrieve the required connection credentials.

**Process**:
- Created a PostgreSQL instance on **Render.com**
- Extracted the connection string, host, port, database name, username, and password
- Used these credentials to connect the local development environment in **Visual Studio Code** to the remote database

---

### 💻 Phase 2: Preparing the Development Environment in Visual Studio Code

**Objective**: Set up a Python-based project environment optimized for data processing and dashboard development.

**Process**:
- Created a dedicated project folder named `police_stops`
- Initialized a Python virtual environment
- Installed essential libraries:
  - `psycopg2-binary` for PostgreSQL connectivity
  - `pandas` for data manipulation
  - `streamlit` and `plotly` for interactive dashboards

---

### 🔌 Phase 3: Python Database Connector (`police.py`)

**Objective**: Programmatically connect the Python application to the PostgreSQL database hosted on Render.com.

**Process**:
- Wrote the connection logic using `psycopg2`
- Stored database credentials using environment variables for security
- Built a reusable `run_query()` function to execute SQL commands and return results via `pandas`

---

### 📥 Phase 4: Data Ingestion and Structuring

**Objective**: Load raw police stop data into memory for analysis.

**Process**:
- Queried the database using `run_query()` to fetch fields such as `violation`, `driver_gender`, `stop_date`, and `stop_time`
- Loaded the results into a **pandas DataFrame** for further analysis

---

### 🧹 Phase 5: Data Cleaning and Preprocessing

**Objective**: Prepare the data for reliable and consistent analysis.

**Process**:
- **Datetime Handling**: Merged `stop_date` and `stop_time` into a unified `stop_datetime` column
- **Missing Values**:
  - Filled `violation` nulls with `'Unknown'`
  - Dropped rows where `driver_gender` was missing
- **Standardization**:
  - Removed duplicate records
  - Cleaned and normalized text formats

---

### 📊 Phase 6: Building the Analytics Dashboard

**Objective**: Visualize trends and demographics through an interactive dashboard.

**Process**:
- Created dynamic visualizations using `plotly.express`
- Integrated charts into a **Streamlit** dashboard via `st.plotly_chart()`
- Displayed metrics including:
  - Stop and arrest frequency over time
  - Demographic insights (gender, age)
  - Violation types and time-based trends

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

| Component     | Tool/Library             |
|---------------|--------------------------|
| Programming   | Python                   |
| Data Analysis | pandas                   |
| Visualization | Streamlit, plotly        |
| Database      | PostgreSQL (Render.com)  |
| DB Connector  | psycopg2-binary          |
| IDE           | Visual Studio Code       |

---
## 🗂️ Project Structure – Police Stop Data Analytics Dashboard

| File/Folder                      | Purpose                                                                 |
|----------------------------------|-------------------------------------------------------------------------|
| `police_stops/`                  | Root directory of the project                                           |
| ├── `.venv/`                     | Python virtual environment (created using Visual Studio Code)           |
| ├── `data/`                      | Folder for local raw data files (e.g., CSVs)                            |
| │     └── `raw_police_stops.csv` | Raw police stop data used for ingestion                                 |
| ├── `police.py`                  | Python script to connect with PostgreSQL and ingest/query data          |
| ├── `streamlit_app.py`           | Main Streamlit dashboard application with visualizations                |
| ├── `requirements.txt`           | Python dependencies (e.g., pandas, psycopg2-binary, plotly, streamlit)  |
| └── `README.md`                  | Project documentation (this file)                                       |

### 🔗 Development Tools & Environment

- **IDE**: Visual Studio Code  
- **Database**: PostgreSQL (hosted on Render.com)  
- **Language**: Python  
- **Libraries**:  
  - `pandas` for data manipulation  
  - `psycopg2-binary` for PostgreSQL connectivity  
  - `plotly` for interactive charts  
  - `streamlit` for dashboard UI

- **Visualization**: Real-time interactive dashboard using `plotly.express` embedded in Streamlit
-  **Hosting**: PostgreSQL instance managed via Render.com and connected from local VS Code environment


## Streamlit App Architecture Overview
###
### +-------------------------+
### |   Streamlit App Launch  |
### +-------------------------+
###             |
###             v
### +--------------------------+
### | Connect to PostgreSQL DB |
### +--------------------------+
###             |
###             v
### +--------------------------+
### |   Sidebar Menu Selection |
### +--------------------------+
###      |       |       |
###      v       v       v
### Vehicle  Violations Analytics
###  Logs        & Trends
###   |             |
###   v             v
### Search or   Charts & Metrics
### Full View     via Plotly
###   |             |
###   v             v
### +--------------------------+
### |   SQL Queries Executed   |
### +--------------------------+
###             |
###             v
### +--------------------------+
### | Results Displayed on UI  |
### +--------------------------+



