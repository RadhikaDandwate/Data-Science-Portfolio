
# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from feature_engine.outliers import Winsorizer

# Load dataset
df = pd.read_csv('mtcars(1).csv')

print("Initial Shape:", df.shape)
print(df.head())

# Check missing values
print("Missing values:\n", df.isnull().sum())

# Fill missing numerical values with mean
num_cols = df.select_dtypes(include=np.number).columns

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())

# Removing duplicates
df.drop_duplicates(inplace=True)
print("After removing duplicates:", df.shape)

# Outlier treatment
# Exclude target column 'mpg' from outlier treatment if predicting mpg
outlier_cols = ['disp', 'hp', 'wt', 'qsec']

for col in outlier_cols:
    sns.boxplot(x=df[col])
    plt.title("Before Outlier Treatment: " + col)
    plt.show()

    winsor = Winsorizer(
        capping_method='iqr',
        tail='both',
        fold=1.5,
        variables=[col]
    )

    df[[col]] = winsor.fit_transform(df[[col]])

    sns.boxplot(x=df[col])
    plt.title("After Outlier Treatment: " + col)
    plt.show()

# Normalization and Standardization
# Exclude target variable mpg
scale_cols = [col for col in num_cols if col != 'mpg']

df_scaled = df.copy()
scaler_std = StandardScaler()
df_scaled[scale_cols] = scaler_std.fit_transform(df_scaled[scale_cols])

df_minmax = df.copy()
scaler_minmax = MinMaxScaler()
df_minmax[scale_cols] = scaler_minmax.fit_transform(df_minmax[scale_cols])

print("Standardized Data:\n", df_scaled.head())
print("Normalized Data:\n", df_minmax.head())

# Skewness transformation
from scipy.stats import skew

for col in scale_cols:
    skew_value = skew(df[col].dropna())
    print(col, "Skewness:", skew_value)

    if skew_value > 1:
        print("Positive skew detected for", col)
        df[col + '_transformed'] = np.log1p(df[col])

    elif skew_value < -1:
        print("Negative skew detected for", col)
        reflected = df[col].max() + 1 - df[col]
        df[col + '_transformed'] = np.log1p(reflected)

    else:
        print("No significant skew for", col)

# Zero Variance Feature Removal
selector = VarianceThreshold(threshold=0.0)

df_var = selector.fit_transform(df.select_dtypes(include=np.number))
selected_cols = df.select_dtypes(include=np.number).columns[
    selector.get_support()
]

df_var = pd.DataFrame(df_var, columns=selected_cols)
print("After removing zero variance features:", df_var.shape)

# Dummy Variables
df_dummies = pd.get_dummies(df, drop_first=True)
print("Original Shape:", df.shape)
print("After Dummy Variables:", df_dummies.shape)

# SMOTE
# Not applied because mtcars is generally used for regression
# and mpg is a continuous target variable.

print("Final Preprocessed Data:\n", df_dummies.head())