# important libraries
# main
import pandas as pd
import numpy as np

# additional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import unicodedata
import re
import requests
from bs4 import BeautifulSoup

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# hypothesis testing
from scipy import stats
import scipy.stats as st
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
from statsmodels.stats.proportion import proportions_ztest # pip install statsmodels
from sklearn.preprocessing import StandardScaler


def data_exploration(df):
    """
    Get some insights on the data.
    param df: pandas DataFrame
    return: 
    - information about number of rows, columns, duplicates, numerical and categorical columns
    - dataframe which consists of column, data type, non-null count, missing values, and unique values. 
    """

    # check number of rows and columns
    shape = df.shape
    print("Number of rows:", shape[0])
    print("Number of columns:", shape[1])

    # check duplicates
    check_duplicates = df.duplicated().sum()
    print("Number of duplicates:", check_duplicates)

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
                        'Column': df.columns,
                        'Data Type': df.dtypes,
                        'Non-Null Count': df.notnull().sum(),
                        'Missing Values': df.isnull().sum(),
                        'Unique Values': df.nunique()
                })

    # Reset index to make 'Column' a regular column
    summary_df.reset_index(drop=True, inplace=True)

    # Display the summary DataFrame
    summary_df
    
    # check numerical columns
    numerical_columns = df.select_dtypes("number").columns
    print("\nNumerical Columns:", numerical_columns)

    # check categorical columns
    categorical_columns = df.select_dtypes("object").columns
    print("\nCategorical Columns:", categorical_columns)

    return summary_df


def standardize_city_name(city):

    """
    standardize city name with character into name without character.
    return: city with standardized name
    """

    # Convert to lowercase
    city = city.lower()
    
    # Remove accents
    city = ''.join(c for c in unicodedata.normalize('NFD', city) # to normalize unicode string separating charactes with accents into base character
                   if unicodedata.category(c) != 'Mn') # check if character is not a non-spacing mark
    
    # Replace special characters with spaces
    city = re.sub(r'[^a-z0-9\s]', ' ', city) # ^ not, lowercase letter(a-z), digit(0-9), or whitespace
    
    # Replace multiple spaces with a single space
    city = re.sub(r'\s+', ' ', city)
    
    # Strip leading and trailing spaces
    city = city.strip()
    
    return city

def analyze_outliers_zscore(df, z_threshold=3):
    """
    Detect outliers using the Z-score method and provide a summary for all numeric columns.
    
    param df: pandas DataFrame
    param z_threshold: Z-score threshold for outlier detection (default 3)
    return: DataFrame with outlier summary for each numeric column
    """
    # Select numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    # Calculate Z-scores for all numeric columns
    z_scores = np.abs(stats.zscore(df[numeric_columns]))
    
    # Prepare summary data
    summary = []
    total_count = len(df)
    
    for column in numeric_columns:
        # Detect outliers
        outliers = df[z_scores[column] >= z_threshold]
        num_outliers = len(outliers)
        percentage_outliers = (num_outliers / total_count) * 100
        
        # Add to summary
        summary.append({
            'Column': column,
            'Number of Outliers': num_outliers,
            'Percentage of Outliers': percentage_outliers,
            'Lower Bound': df[column].mean() - z_threshold * df[column].std(),
            'Upper Bound': df[column].mean() + z_threshold * df[column].std(),
            'Min Outlier': outliers[column].min() if not outliers.empty else None,
            'Max Outlier': outliers[column].max() if not outliers.empty else None
        })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary)
    
    # Sort by percentage of outliers (descending)
    summary_df = summary_df.sort_values('Percentage of Outliers', ascending=False)
    
    # Format percentage for readability
    summary_df['Percentage of Outliers'] = summary_df['Percentage of Outliers'].round(2).astype(str) + '%'
    
    return summary_df


def remove_outliers_zscore(df, z_threshold=3):
  
    """
    Remove outliers with Z-score method
    param df: pandas DataFrame
    return: DataFrame with no outliers.
    """

	# select numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Make a copy of the dataframe with only numeric columns
    df_numeric = df[numeric_columns].copy()

    # Calculate Z-scores for the specified columns
    z_scores = np.abs(stats.zscore(df_numeric))

    # Filter rows where Z-scores are below the threshold
    df_no_outliers = df[(z_scores < z_threshold).all(axis=1)]
  
    print(f"Removed {len(df) - len(df_no_outliers)} rows")
  
    return df_no_outliers


def plot_distributions(df):

    """
    Plot distribution of numerical columns.
    param df: pandas DataFrame
    return: histogram and boxplot.
    """

	# Select numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for column in numeric_columns:
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        sns.histplot(df[column], kde=True, ax=ax[0])
        sns.boxplot(x=df[column], ax=ax[1])
        ax[0].set_title(f'Distribution of {column}')
        ax[1].set_title(f'Boxplot of {column}')
        plt.show()



"""EDA"""


def univariate_numerical(df):
    """
    Plot distribution of numerical columns.
    param df: pandas DataFrame
    return: histogram and boxplot side by side for each numerical column, and summary statistics.
    """

    df_num = df.select_dtypes(include=[np.number])
    
    # Calculate statistics
    summary_stats = []
    for col in df_num.columns:
        stats = {
            'Column': col,
            'Mean': round(df_num[col].mean(), 2),
            'Median': round(df_num[col].median(), 2),
            'Mode': round(df_num[col].mode().iloc[0], 2),
            'Variance': round(df_num[col].var(), 2),
            'Standard Deviation': round(df_num[col].std(), 2),
            'Min Value': df_num[col].min(),
            'Max Value': df_num[col].max(),
            'Range': df_num[col].max() - df_num[col].min(),
            'Interquartile Range': df_num[col].quantile(0.75) - df_num[col].quantile(0.25),
            'Skewness': round(df_num[col].skew(), 2),
            'Kurtosis': round(df_num[col].kurtosis(), 2)
        }
        summary_stats.append(stats)

    summary_df = pd.DataFrame(summary_stats)

    # Visualization
    for col in df_num.columns:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # Side by side, reduced size

        # Histogram plot
        sns.histplot(data=df_num, x=col, ax=ax1, kde=True, bins=20, color="skyblue")
        ax1.set_title(f'Histogram of {col}')

        # Box plot
        sns.boxplot(data=df_num, x=col, ax=ax2, color="skyblue")
        ax2.set_title(f'Box Plot of {col}')

        plt.tight_layout()
        plt.show()
    
    return summary_df


def summary_categorical_correlation(df, target_column):

    categorical_columns = df.select_dtypes(['object', 'category']).columns
    categorical_columns = [col for col in categorical_columns if col != target_column]

    results = []

    for column in categorical_columns:
        crosstab_result = pd.crosstab(df[column], df[target_column])

        # Chi-square test
        chi2_statistic, chi2_p_value, _, _ = chi2_contingency(crosstab_result)

        # Cramer's V
        cramer = association(crosstab_result, method="cramer")

        # Append all results
        results.append({
            'Column': column,
            'Chi2 p-value': chi2_p_value,
            'Cramer V': cramer
        })
    
    # Create a DataFrame for results
    results_df = pd.DataFrame(results)

    return results_df