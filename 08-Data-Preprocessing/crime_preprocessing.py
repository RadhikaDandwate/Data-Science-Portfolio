

# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from feature_engine.outliers import Winsorizer

# Load dataset
df = pd.read_csv('crime_data (1)(2).csv')

print("Initial Shape:", df.shape)
print(df.head())

# Rename first column
df.rename(columns={'Unnamed: 0': 'State'}, inplace=True)

# Check missing values
print("Missing values:\n", df.isnull().sum())

# Fill missing numerical values with mean
num_cols = df.select_dtypes(include=np.number).columns

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())

# Fill missing categorical values with mode
cat_cols = df.select_dtypes(include=['object', 'category']).columns

for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# Removing duplicates
df.drop_duplicates(inplace=True)
print("After removing duplicates:", df.shape)

# Outlier treatment
outlier_cols = ['Murder', 'Assault', 'UrbanPop', 'Rape']

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
scale_cols = ['Murder', 'Assault', 'UrbanPop', 'Rape']

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
        df[col + '_transformed'] = np.log1p(df[col])

    elif skew_value < -1:
        reflected = df[col].max() + 1 - df[col]
        df[col + '_transformed'] = np.log1p(reflected)

    else:
        print("No significant skew for", col)

# Zero Variance Feature Removal
numeric_df = df.select_dtypes(include=np.number)

selector = VarianceThreshold(threshold=0.0)
df_var_array = selector.fit_transform(numeric_df)

selected_cols = numeric_df.columns[selector.get_support()]
df_var = pd.DataFrame(df_var_array, columns=selected_cols)

print("After removing zero variance features:", df_var.shape)

# Dummy Variables
df_dummies = pd.get_dummies(df, drop_first=True)

print("Original Shape:", df.shape)
print("After Dummy Variables:", df_dummies.shape)

# SMOTE
# Not applied because this dataset does not have a
# specified classification target column.

print("Final Preprocessed Data:\n", df_dummies.head())