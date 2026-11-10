# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 18:31:54 2026

@author: Gauri
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


# load the titanic dataset
df = sns.load_dataset('titanic')
print('initial shape:' , df.shape)
df.head()

# CHeck missing values
print("missing values: ", df.isnull().sum())

# Drop columns with too many missing values
df.drop(columns=['deck'],inplace=True)

#Fill categorical missing values with mode, numerical with mean
cat_cols = df.select_dtypes(include='object').columns
num_cols = df.select_dtypes(include=['int64','float64']).columns

for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

'''
why [0] is required?
fillna() needs ONE single value
[0] selects the first most frequent value
Ensures the code always works, even if multiple modes exits
'''

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())
    
    
#Removing duplicates
df.drop_duplicates(inplace=True)
print("After removing duplicates:", df.shape)

##  OUTLIER Treatment

#plot boxplots for each numeric column
sns.boxplot(df.age)
sns.boxplot(df.fare)

from feature_engine.outliers import Winsorizer

winsor = Winsorizer(
    capping_method='iqr',
    tail='both',
    fold=1.5,
    variables=['age']
    )

df_t = winsor.fit_transform(df[['age']])
sns.boxplot(df['age'])
sns.boxplot(df_t['age'])

# for FARE
winsor = Winsorizer(
    capping_method='iqr',
    tail='both',
    fold=1.5,
    variables=['fare']
    )

df_t = winsor.fit_transform(df[['fare']])
sns.boxplot(df['fare'])
sns.boxplot(df_t['fare'])


## Normalization and Standardization
# Make a copy for demonstration
df_scaled = df.copy()

# Standardozation (mean=0 , std=1)
scaler_std = StandardScaler()
df_scaled[num_cols] = scaler_std.fit_transform(df_scaled[num_cols])

# Normalization (min = 0, max = 1)
scaler_minmax = df.copy()
df_minmax = df.copy()
df_minmax[num_cols] = scaler_minmax.fit_transform(df_minmax[num_cols])



from scipy.stats import skew

from sklearn.preprocessing import skew

from sklearn.preprocessing import PowerTransformer
# Calculate skewness of the fare column
# dropna() removes missing values
skew_value = skew(df['fare'].dropna())

# Print skew value for understanding
print("skewness value:", skew_value)

# if skewness is greater than 0, data is positively(right) skewed
if skew_value > 0:
    
    # inform user that right skew is detected
    print("positive skew detected- applying log transform")
    
    # apply log(1 + x) transformation
    # log1p is used to safely handle zero values
    # this compresses large values on the right side
    df['fare_transformed'] = np.log1p(df['fare'])
    
# if skewness is less than 0, data is already symetric
else:
    
    # inform user that no transformation is needed
    print("No significant skew -> no transformation applied")
    
    # keep original values unchanged
    df['fare_transformed'] = df['fare']
    
# plot the final transformed distribution
# KDE curve helps visualize smooth distribution
sns.histplot(df['fare'],kde=True)
sns.histplot(df['fare_transformed'], kde=True)\
  .set_title("Final Transformed Fare")


# zero variance feature removel
df['constant'] = 1 

from sklearn.feature_selection import VarianceThreshold

# create object
selector = VarianceThreshold(threshold=0.0)

# Appply only to numeric features
df_var = selector.fit_transform(df.select_dtypes(include=['folat64','int64']))


