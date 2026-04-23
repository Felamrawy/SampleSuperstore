# 🏬 Superstore Executive Performance Analysis

This repository contains a data-driven evaluation of a retail superstore's performance. The project moves from raw data exploration to a strategic decision-support tool, identifying specific products, regions, and pricing strategies that impact the bottom line.

## 📌 Project Goals
* **Identify Profitability Drivers:** Pinpoint which product categories and sub-categories generate the most revenue vs. profit.
* **Detect Inefficiencies:** Uncover specific regions and products (like Tables and Bookcases) that are causing significant losses.
* **Pricing Strategy:** Evaluate the correlation between discounts and profit margins.
* **Geographic Analysis:** Map out state-level performance to identify high-loss areas like Texas and Illinois.

## 📂 Project Structure
* `EDA_SampleSuperstore.ipynb`: The core exploratory notebook containing data cleaning, hypothesis testing, and statistical visualization.
* `dash_superstores.py`: A production-ready Dash application that operationalizes the EDA findings into an interactive executive dashboard.
* `superstore_cleaned.csv`: The cleaned dataset used for driving the dashboard.
* `requirements.txt`: Necessary Python libraries to run the project.

## 🚀 Key Insights
* **The Furniture Problem:** The analysis reveals that the *Furniture* category, specifically **Tables** and **Bookcases**, is a primary driver of financial loss.
* **Discount Thresholds:** High discounts (above 20%) show a strong correlation with negative profit margins, suggesting a need for a revised pricing strategy.
* **Regional Disparities:** States like **Texas and Illinois** show significant losses, potentially due to shipping distances or local market competition.

## 📊 Interactive Dashboard Features
The dashboard (`dash_superstores.py`) is built using **Dash** and **Plotly** to provide:
* **KPI Overviews:** Total Sales, Total Profit, and overall Profit Margin.
* **Geographic Map:** A Choropleth map identifying profit/loss by state.
* **Profitability Analysis:** Interactive bar charts showing profit margins by sub-category.
* **Correlation Scatters:** Visualizing the impact of discounts on individual sales performance.

## ⚙️ Setup & Installation

**Clone the repository:**
   ```bash
   git clone [https://github.com/Felamrawy/pupg.git](https://github.com/Felamrawy/pupg.git)
   cd pupg
```

**Install the libraries:**
   ```bash
   pip install -r requirements.txt
   ```

**Run the Dashboard:**
   ```bash
   python dash_superstores.py
   ```

    

## 🛠️ Built With
* **Pandas & NumPy:** Data manipulation.
* **Plotly & Matplotlib:** Advanced data visualization.
* **Dash & Dash Bootstrap Components:** Web application framework.
  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-orange.svg)
![Dash](https://img.shields.io/badge/Framework-Dash-008080.svg)

**Developed by [Felamrawy](https://github.com/Felamrawy)**