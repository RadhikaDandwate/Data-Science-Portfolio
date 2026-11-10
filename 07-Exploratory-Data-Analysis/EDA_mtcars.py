import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('mtcars(1).csv')

df.dtypes

# Shape and Size
print("Shape of dataset:", df.shape)
print("Size of dataset:", df.size)

print(df.describe())

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
for col in ['mpg', 'disp', 'hp', 'wt']:
    sns.histplot(df[col], kde=True)
    plt.title(f'Histogram of {col}')
    plt.show()

# Scatter Plot
sns.scatterplot(data=df, x='wt', y='mpg')
plt.title("Weight vs Mileage")
plt.show()

# Joint Plot
sns.jointplot(data=df, x='wt', y='mpg')
plt.show()

# Pair Plot
sns.pairplot(df[['mpg', 'disp', 'hp', 'wt', 'qsec']])
plt.show()

# Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, orient='h')
plt.title("Boxplot of Car Features")
plt.show()

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
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