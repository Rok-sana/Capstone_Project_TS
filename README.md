# Capstone_Project_TS

# Business Case #


## Introduction

In this project, I've analyzed and forecasted sales data for Walmart across various stores and product categories. Here's a detailed overview based on the findings and questions posed:

## Business Metrics and Forecasting

Business Metrics Importance: Key metrics for Walmart include sales volume, revenue, profit margins, and inventory turnover. Forecasting helps Walmart plan inventory, optimize staffing, and anticipate customer demand.

Improving Business Metrics: Accurate forecasting allows Walmart to reduce stockouts, optimize pricing strategies, and improve overall operational efficiency.

ML Metrics vs. Business Metrics: Metrics like RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error) used in this competition directly measure forecast accuracy. These relate to business metrics by ensuring predictions align closely with actual sales, reducing forecasting errors.

Designing Better ML Metrics: A better ML metric could focus on capturing errors' financial impact, such as weighted errors by sales volume or revenue impact, to directly relate model performance to business outcomes.

## Managerial Decisions and Model Outputs

Controlled Variables: Walmart can control pricing, inventory levels, promotions, and staffing across stores. These influence sales directly.

Uncontrolled Variables: External factors like economic conditions, weather, and competitor actions impact sales but are beyond direct control.

Production Use of Model: If deployed in production, the model could guide decisions on inventory stocking levels, promotional timing, and pricing adjustments. These forecasts influence variables like profitability and customer satisfaction.

High-Level Analyst Perspective and Sensitivity Analysis

Price Elasticity of Demand: Using the model, I would calculate price elasticity by examining how changes in price affect sales volume for specific products and aggregate across stores. This helps in optimizing pricing strategies.

Impact on Walmart's Bottom Line: Analysts use price elasticity to determine optimal pricing levels that maximize revenue without sacrificing sales volume. This insight can significantly improve profit margins.

## SNAP Program Analysis

SNAP Program Influence: The model estimates SNAP days increase sales by approximately 10%, showing higher demand during these periods compared to non-SNAP days.

Naive vs. Model Estimates: Naive estimates might overlook nuances captured by the model, such as regional variations or product-specific impacts, leading to less accurate predictions of SNAP day effects on sales.

## Competition Reflection and Improvements

Improving the Competition: To enhance its relevance for Walmart, the competition could include challenges on integrating external data sources (like weather or economic indicators), improving real-time forecasting capabilities, and incorporating supply chain dynamics for more holistic predictions.

Final Thoughts: This competition provided valuable insights into retail forecasting challenges. To further assist Walmart, future competitions could focus on integrating more real-world complexities and enhancing model interpretability for actionable insights.

## Conclusions ##

Based on the analysis of Walmart sales data across states and stores from January 29th, 2011, to April 24th, 2016, we observe an overall increasing trend in sales over the years. Sales are observed to be zero on the very first day of each year due to store closures on New Year's Day. Each year shows seasonal patterns, and the time series within each year is stationary. Monthly sales tend to be highest in March and lowest in November. Sales are highest on weekends compared to weekdays (Monday to Thursday), with Fridays slightly higher than other weekdays.

California has the highest sales and revenue generated, while Texas and Wisconsin show similar levels of sales and revenue. The Food category accounts for 70% of sales but contributes only 58% of the revenue, indicating lower average prices compared to other categories. Sales are slightly higher on SNAP (Supplemental Nutrition Assistance Program) days compared to non-SNAP days across all states.

Each product category exhibits non-periodic daily sales patterns, with Food products showing higher overall sales and revenue due to their larger variety. Sales increase during sporting and cultural events but decrease on national holidays. Sales are higher at the beginning of the month and decrease gradually towards the end. SNAP days show an increase in sales, ranging from at least 4% to as high as 30% compared to non-SNAP days.

This analysis highlights the complex and varied sales patterns across different dimensions such as time, category, state, and event influence at Walmart stores.

The model and metrics are listed below. The best performing have LgbmRegressor  model.


| Model                                         |   WRMSSE |
|-----------------------------------------------|----------|
| Seasonal Naive Model                          |   0.7524 |
| Moving Average                                |   1.6915 |
| LgbmRegressor                                 |   0.6076 |
| SGDRegressor                                  |   1.1055 |
