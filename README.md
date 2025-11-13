# E-Commerce YTD Sales Analysis

Comprehensive Year-over-Year sales analysis for an Indian e-commerce platform with **YTD (Year-to-Date)**, **PYTD (Previous Year-to-Date)**, and **P1YTD (Prior Year-to-Date)** calculations, time series forecasting, and data visualizations.

## 📈 Project Overview

This data analytics project analyzes 3 fiscal years (FY 2022-23, 2023-24, 2024-25) of e-commerce sales data for an Indian platform, comparing current performance against previous years to identify trends, seasonality patterns, and growth opportunities.

### Key Metrics
- **YTD**: Current fiscal year sales up to analysis date
- **PYTD**: Previous fiscal year sales for the same period
- **P1YTD**: Two fiscal years ago sales for the same period
- **Delta**: Difference between YTD and PYTD (growth/decline)

## ✨ Features

### 1. Synthetic Data Generation
- 📅 **3 Years**: FY 2022-23, 2023-24, 2024-25 (April-March fiscal year)
- 📍 **8 Cities**: Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad
- 📚 **10 Products**: Electronics, Fashion, Home & Kitchen categories
- 👥 **4 Segments**: Premium, Mid-Tier, Budget, First-Time customers
- 🎉 **Realistic Seasonality**: Diwali, Independence Day, Republic Day, New Year, Black Friday
- 🏷️ **Promotional Events**: Quarterly sales, festival discounts
- 📊 **200,000+ Records**: Daily transaction-level data

### 2. YTD/PYTD/P1YTD Calculations
- Automatic fiscal year detection (Indian FY: April-March)
- Product-level performance metrics
- Growth/decline percentage calculations
- Performance classification (Growing/Declining/Stable)

### 3. Advanced Visualizations

#### 🔴🟢 **Signature Scatter Plot**
- **X-axis**: YTD Sales
- **Y-axis**: Delta (YTD - PYTD)
- **Color Coding**: 🔴 RED for declining products, 🟢 GREEN for growing products
- **Bubble Size**: Proportional to absolute delta value
- Interactive Plotly charts

#### Other Visualizations
- 📋 Bar Charts: YTD vs PYTD vs P1YTD comparison
- 📈 Time Series: Monthly trends by product
- 🔥 Heatmaps: Month-over-month sales patterns
- 📉 Growth Percentage: Product performance ranking
- 🔍 Seasonal Decomposition: Trend, seasonality, residual analysis

### 4. Statistical Modeling
- **Linear Regression**: Sales trend analysis
- **Moving Averages**: 7-day and 30-day MA for seasonality
- **Time Series Forecasting**: ARIMA-ready data structure
- **Model Evaluation**: R² score, RMSE metrics

### 5. Business Insights
- Product performance segmentation
- Seasonality pattern identification
- Strategic recommendations for declining products
- Growth opportunity identification

## 💾 Project Structure

```
Ecommerce-YTD-Sales-Analysis/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── data_generator.py            # Synthetic data generation
├── ytd_calculations.py          # YTD/PYTD/P1YTD metrics calculator
├── visualizations.py            # Visualization functions
├── analysis.ipynb               # Comprehensive Jupyter notebook
└── LICENSE                      # MIT License
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abhinad/Ecommerce-YTD-Sales-Analysis.git
cd Ecommerce-YTD-Sales-Analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Run Jupyter Notebook (Recommended)
```bash
jupyter notebook analysis.ipynb
```
This will open the comprehensive analysis notebook with step-by-step execution.

#### Option 2: Run Python Scripts Individually

**Generate Data:**
```python
python data_generator.py
```

**Calculate YTD Metrics:**
```python
import data_generator
import ytd_calculations

# Generate data
sales_df = data_generator.generate_complete_dataset()

# Calculate metrics
ytd_metrics = ytd_calculations.calculate_ytd_metrics(sales_df)
ytd_with_deltas = ytd_calculations.calculate_deltas(ytd_metrics)

print(ytd_with_deltas)
```

**Create Visualizations:**
```python
import visualizations

# Signature scatter plot with RED/GREEN color coding
fig = visualizations.plot_ytd_scatter_with_delta(ytd_with_deltas)

# Bar chart comparison
fig = visualizations.plot_ytd_comparison_bars(ytd_with_deltas)

# Growth percentage
fig = visualizations.plot_growth_percentage(ytd_with_deltas)
```

## 📊 Sample Outputs

### YTD Metrics Summary
```
Product Performance:
- Growing Products: 6/10 (60%)
- Declining Products: 4/10 (40%)

Top Growing Product:
- Product: Samsung Galaxy S23
- YTD Sales: ₹12,45,000
- Delta: +₹2,15,000 (20.9% growth)

Top Declining Product:
- Product: Winter Jacket
- YTD Sales: ₹4,32,000
- Delta: -₹1,08,000 (-20.0% decline)
```

### Key Findings
1. **Seasonality Impact**: 40-60% sales spike during festival seasons
2. **Electronics Growth**: 25% YoY growth in Electronics category
3. **Regional Variance**: Mumbai and Bangalore lead with 35% of total sales
4. **Customer Segments**: Premium segment shows 30% higher growth

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Static visualizations
- **Plotly**: Interactive charts (scatter plots, bar charts)
- **Scikit-learn**: Linear regression modeling
- **Statsmodels**: Time series analysis
- **Jupyter**: Interactive notebook environment

## 📝 Key Insights for Business Strategy

### For Growing Products (🟢)
- **Action**: Increase inventory allocation
- **Action**: Expand marketing budget
- **Action**: Leverage success patterns for similar products

### For Declining Products (🔴)
- **Action**: Investigate root causes (pricing, competition, trends)
- **Action**: Consider promotional campaigns
- **Action**: Evaluate product-market fit

### Seasonal Planning
- **Diwali (Oct-Nov)**: 60% sales spike - prepare 8 weeks ahead
- **Independence Day (Aug)**: 30% spike - focus on patriotic themes
- **Year-End (Dec-Jan)**: 45% spike - clearance + new year offers

## 🎓 Use Cases

- 🎯 **Portfolio Project**: Showcase data analytics and Python skills
- 💼 **Business Intelligence**: Real-world YTD analysis methodology
- 📚 **Learning**: Understand time series, forecasting, visualization
- 🛠️ **Template**: Adapt for actual business data

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Abhinad**
- GitHub: [@Abhinad](https://github.com/Abhinad)
- Project: Data Analytics Portfolio

## 🚀 Future Enhancements

- [ ] ARIMA/Prophet time series forecasting implementation
- [ ] Customer lifetime value (CLV) analysis
- [ ] Market basket analysis for product recommendations
- [ ] Dashboard creation with Plotly Dash or Streamlit
- [ ] Integration with Power BI/Tableau for BI reporting
- [ ] SQL database integration for data storage

## 🔗 Related Projects

- [E-Commerce Sales Analytics](https://github.com/Abhinad/Ecommerce-Sales-Analytics) - Related sales analytics project

---

**⭐ If you found this project helpful, please consider giving it a star!**

**👍 Contributions, issues, and feature requests are welcome!**
