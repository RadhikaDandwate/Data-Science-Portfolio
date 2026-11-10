import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Company_Data (2).csv')

df.dtypes

# Shape and Size
print("Shape of dataset:", df.shape)
print("Size of dataset:", df.size)

print(df.describe(include='all'))

# 1 First Moment: Mean
mean_values = df.mean(numeric_only=True)
print("\nMean (First Moment):\n", mean_values)

# 2 Second Moment: Variance/Standard Deviation
var_values = df.var(numeric_only=True)
std_values = df.std(numeric_only=True)
print("\nVariance (Second Moment):\n", var_values)
print("\nStandard Deviation:\n", std_values)

# 3 Third Moment: Skewness
skew_values = df.skew(numeric_only=True)
print("\nSkewness (Third Moment):\n", skew_values)

# 4 Fourth Moment: Kurtosis
kurt_values = df.kurtosis(numeric_only=True)
print("\nKurtosis (Fourth Moment):\n", kurt_values)

# Histograms
for col in ['Sales', 'CompPrice', 'Advertising', 'Price']:
    sns.histplot(df[col], kde=True)
    plt.title(f'Histogram of {col}')
    plt.show()

# Count plots for categorical columns
for col in ['ShelveLoc', 'Urban', 'US']:
    plt.figure(figsize=(7, 4))
    sns.countplot(data=df, x=col)
    plt.title(f'Count Plot of {col}')
    plt.show()

# Scatter Plot
sns.scatterplot(data=df, x='Price', y='Sales', hue='ShelveLoc')
plt.title("Price vs Sales")
plt.show()

# Joint Plot
sns.jointplot(data=df, x='Price', y='Sales')
plt.show()

# Pair Plot
sns.pairplot(df[['Sales', 'CompPrice', 'Income',
                 'Advertising', 'Price', 'Age']])
plt.show()

# Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['Sales', 'CompPrice', 'Income',
                     'Advertising', 'Price', 'Age']], orient='h')
plt.title("Boxplot of Company Data")
plt.show()

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include=np.number).corr(),
            annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.show()

# PDF and CDF
num_cols = df.select_dtypes(include=np.number).columns

for col in num_cols:
    plt.figure(figsize=(12, 5))

    # PDF
    plt.subplot(1, 2, 1)
    sns.kdeplot(df[col], fill=True, color='blue')
    plt.title(f'PDF of {col}')

    # CDF
    plt.subplot(1, 2, 2)
    sorted_vals = np.sort(df[col])
    y_vals = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)
    plt.plot(sorted_vals, y_vals, marker='.', linestyle='none',
             color='green')
    plt.title(f'CDF of {col}')

    plt.tight_layout()
    plt.show()