# Brazilian e-commerce analysis

## Project Overview
This project involves analyzing a Brazilian e-commerce dataset from Olist, a multi-marketplace e-commerce platform. The analysis focuses on sales performance, customer experience, and delivery accuracy, using various data science techniques including machine learning for delivery prediction and sentiment analysis. The results are visualized in a PowerBI dashboard, and a prediction tool is built with Streamlit to provide real-time sales and delivery date predictions. 

Here is the project overview flow diagram. <br>
![Project Overview](/resources/charts/project_flow_diagram.png)

## Data
The dataset includes information on 100,000 orders made between 2016 and 2018 across multiple marketplaces in Brazil (source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)). The data covers various dimensions such as order status, price, payment, freight performance, customer location, product attributes, and customer reviews. Additional data on Brazilian state populations, obtained via web scraping from [Wikipedia](https://en.wikipedia.org/wiki/Federative_units_of_Brazil), is also included.

The illustration below shows the relationship of the data in the database. <br>
![Database Overview](/resources/charts/database_overview.png)


## Key Performance Indicator (KPI) 
**1. Sales Growth Rate** <br>

The goal of this KPI is to measure the increase in total sales over a specified period, indicating the effectiveness of market strategies.

Customer Sentiment and Emotion Analysis: Assesses customer feedback through sentiment and emotion analysis to gauge customer satisfaction and identify areas for improvement.


**2. On-Time Delivery Rate** <br>

The purpose of this KPI is to the percentage of orders delivered on or before the estimated delivery date, reflecting logistics performance.


**3. Customer Sentiment and Emotion Analysis** <br>

This KPI assesses customer feedback through sentiment and emotion analysis to gauge customer satisfaction and identify areas for improvement.


## Conclusion
- Olist has achieved a 20% sales growth, indicating effective market strategies and strong market demand.
  
- Peak order times is Monday, 11 am-16 pm, highlighting customer purchasing patterns.
  
- The on-time delivery rate of 92% shows good performance in meeting delivery expectations, leaving room for improvement either on carrier or seller performance.
  
- The average review score of 4.1/5 indicates potential for improvement on the

## Recommendations
- Develop targeted strategies to replicate the success of top-performing products and sellers.
  
- Implement special promotions during off-peak hours to potentially increase overall sales.
  
- Establish a performance improvement program for sellers and carriers who underperform.
  
- Enhance the app’s user experience by addressing customer feedback to improve ratings and overall satisfaction.

## Additional links
- [Presentation slides](https://docs.google.com/presentation/d/1bc8dZVfOTsr_bVjOY3AXwJCtHIMQDww6qgk1fFb-QGA/edit#slide=id.g2f54d952ab1_0_700)
- [PowerBI Dashboard](resources/PowerBI_dashboard/e-commerce_dashboard)
- [Streamlit Repository](https://github.com/RosaEvasari/e-commerce-streamlit)
- [Kanban of Project Management](https://trello.com/b/MCTPibpJ/project-management-of-final-project)
