# 🚀 SpaceX Falcon 9 First Stage Landing Prediction

## Project Overview

This repository contains a comprehensive data science project focused on predicting the success of the SpaceX Falcon 9 rocket's first stage landing.

The project follows a complete data science lifecycle: from collecting raw launch data via web scraping and cleaning it, to performing advanced Exploratory Data Analysis (EDA) using SQL and Folium for visualization, and finally, building and evaluating four different classification models to predict landing success.

**The goal is to determine the optimal conditions for a successful first-stage recovery, which is critical for reducing launch costs.**

## 💾 Project Structure & Labs Completed

This project is organized into several sequential notebooks, each representing a key phase of the data science process.

| Phase | Notebooks | Description |
| ----- | ----- | ----- |
| **1. Data Engineering** | `Jupyter-lab-webscraping.ipynb` | Scraped raw data from the SpaceX website (Wikipedia) to gather historical launch records, including key metrics like date, booster version, payload, and orbit. |
| **2. Data Wrangling** | `Jupyter-lab-spacex-data-wrangling.ipynb` | Cleaned, transformed, and prepared the raw data for analysis, handling missing values and engineering the crucial binary target variable (`Class`: 1 for Success, 0 for Failure). |
| **3. SQL & EDA** | `Jupyter-lab-sql-coursera-sqlite.ipynb` | Used SQL queries to perform detailed Exploratory Data Analysis (EDA) and extract key statistics from the cleaned dataset. |
| **4. Visualization (Geospatial & Trend)** | `lab_jupyter_launch_site_location.ipynb` | Explored launch site geography using the **Folium** library to visualize locations and proximity to infrastructure (coastline, highways). |
| **5. Machine Learning Prediction** | `SpaceX_Machine Learning Prediction_Part_5 (2).ipynb` | Built, tuned, and evaluated four different classification models to predict landing success. |

## 📈 Key Findings and Insights

### A. Exploratory Data Analysis (SQL & Visualization)

The SQL and visualization phases yielded critical operational insights:

| Insight | Key Metric/Finding | SQL Query Example |
| ----- | ----- | ----- |
| **Launch Sites** | **4 unique sites** were identified: CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, and CCAFS SLC-40. The majority of launches (46 out of 56) are clustered on the **East Coast (Florida)**. | `SELECT DISTINCT Launch_Site FROM SPACEXTABLE;` |
| **Success Trend** | The average launch success rate showed a strong positive trend, rising from $0.0$ in 2010 to consistently over $0.8$ in later years, peaking near $0.9$ in 2019. | `SELECT AVG(Class) FROM SPACEXTABLE GROUP BY YEAR(Date);` |
| **Payload & Orbit** | Most launches target **LEO** and **GTO**. The single heaviest payloads were carried by **F9 B5** variants. | `SELECT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS_KG_ = (SELECT MAX(PAYLOAD_MASS_KG_) FROM SPACEXTABLE);` |
| **First Success** | The **first successful ground pad landing** occurred on **2015-12-22**. | `SELECT MIN(Date) FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (ground pad)';` |

### B. Machine Learning Prediction Results

Four classification models were built using standardized, one-hot encoded data and tuned using `GridSearchCV` (cv=10).

| Model | Test Accuracy | Best Score (Validation) | Best Parameters |
| ----- | ----- | ----- | ----- |
| **Logistic Regression** | **0.8333** | $0.8464$ | `{'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}` |
| **SVM (Support Vector Machine)** | **0.8333** | $0.8482$ | `{'C': 1.0, 'gamma': 0.0316, 'kernel': 'sigmoid'}` |
| **K-Nearest Neighbors (KNN)** | **0.8333** | $0.8482$ | `{'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}` |
| **Decision Tree** | $0.7222$ | $0.8875$ | `{'criterion': 'entropy', 'max_depth': 12, 'max_features': 'sqrt', ...}` |

**Conclusion:**

The **Logistic Regression, SVM, and KNN** models performed equally well on the independent test set, with a top accuracy of **83.33%**. The primary predictive challenge for these models was minimizing **False Positives** (predicting success when the launch actually failed).

## 🛠️ Requirements

The analysis was primarily conducted using Python and Jupyter notebooks. Key libraries include:

* `pandas` and `numpy` for data manipulation.

* `matplotlib` and `seaborn` for plotting.

* `sqlite3` for SQL queries (via `sqlite` module or magic commands).

* `Folium` for geospatial visualization.

* `scikit-learn` (`sklearn`) for machine learning models (LogisticRegression, SVC, DecisionTreeClassifier, KNeighborsClassifier, GridSearchCV).

## 🔗 Repository Contents

* `SpaceX_Machine Learning Prediction_Part_5 (2).ipynb`: Final notebook containing the standardized data, model training, tuning, and accuracy evaluation.

* `lab_jupyter_launch_site_location.ipynb`: Notebook for Folium map visualization.

* `jupyter-lab-webscraping.ipynb`: Initial data collection notebook.

* `jupyter-lab-spacex-data-wrangling.ipynb`: Data cleaning and feature engineering.

* `jupyter-lab-sql-coursera-sqlite.ipynb`: Notebook demonstrating SQL queries for EDA.
