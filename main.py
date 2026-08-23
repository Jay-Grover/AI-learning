import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("data/raw/bank-additional-full.csv", sep=";")

# print(df.head()) # gives a look at data
# print(df.shape) # just (row, col)
# print(df.info()) # gives dtype of each col memory usage etc

# print("\nColumn names:")
# print(df.columns)

# print("\nData types:")
# print(df.dtypes)
#
# print("\nMissing values:")
# print(df.isnull().sum())

# this above thing returns 0 for all cols but there is placeholder when seem in head as "unknown" for null values
# so we try to understand each column now
# print(df["job"].value_counts())
# print(df["education"].value_counts())
# print(df["default"].value_counts())

# Now we get like above for all the columns that are of object datatype
# categorical_columns = df.select_dtypes(include="object").columns
#
# for col in categorical_columns:
#     print(f"\n--- {col} ---")
#     print(df[col].value_counts())

# print("\nDuplicate rows:")
# print(df.duplicated().sum()) # df.duplicate returns true if a row is repeated and .sum gives sum for all the true values

# inspect duplicate rows
# duplicates = df[df.duplicated()]
#
# print(duplicates)
# df.eq(df.loc[1266]) comapres each row with 1266 tuple .all asks are all columns equal for this row
# print(df[df.eq(df.loc[1266]).all(axis=1)])  # returns the original and duplicate row

print("Before:", df.shape)
df = df.drop_duplicates()
print("After:", df.shape)
print(df.duplicated().sum())

# numeric rows analysis
# print("\nNumerical summary:")
# print(df.describe()) # here we have many one is count and returns total non Nan values
#                age      duration      campaign         pdays      previous  emp.var.rate  cons.price.idx  cons.conf.idx     euribor3m   nr.employed
# count  41176.00000  41176.000000  41176.000000  41176.000000  41176.000000  41176.000000    41176.000000   41176.000000  41176.000000  41176.000000
# mean      40.02380    258.315815      2.567879    962.464810      0.173013      0.081922       93.575720     -40.502863      3.621293   5167.034870
# std       10.42068    259.305321      2.770318    186.937102      0.494964      1.570883        0.578839       4.627860      1.734437     72.251364
# min       17.00000      0.000000      1.000000      0.000000      0.000000     -3.400000       92.201000     -50.800000      0.634000   4963.600000
# 25%       32.00000    102.000000      1.000000    999.000000      0.000000     -1.800000       93.075000     -42.700000      1.344000   5099.100000
# 50%       38.00000    180.000000      2.000000    999.000000      0.000000      1.100000       93.749000     -41.800000      4.857000   5191.000000
# 75%       47.00000    319.000000      3.000000    999.000000      0.000000      1.400000       93.994000     -36.400000      4.961000   5228.100000
# max       98.00000   4918.000000     56.000000    999.000000      7.000000      1.400000       94.767000     -26.900000      5.045000   5228.100000

# now we want to understand outliers for above some columns like duration(max = 4918) very high from mean or pdays
# print(df["pdays"].value_counts().head(10)) # shows how frequently differnt pday value occurs
# print("pdays == 999:", (df["pdays"] == 999).sum()) # gives count of tuple with pdays = 999 values

# what we come to know is that 999 is a dummy value for that col if the customer is not contacted
# df["previously_contacted"] = (df["pdays"] != 999).astype(int) # so we may create a new feature so reduce bias for 999

# print(df["duration"].describe())
# print("Duration > 1000:", (df["duration"] > 1000).sum()) # around 900 rows so not an outlier
# print("Duration == 0:", (df["duration"] == 0).sum()) # 4 rows need to see these maybe never contacted

df["previously_contacted"] = (df["pdays"] != 999).astype(int)
# print(df["previously_contacted"].value_counts())

# so we understood that uration is of current call and we cant use it as a feature to train model
# also pdays has 999 values as default rather we create a col days_since_contact and keep 999 as Nan
df["days_since_contact"] = df["pdays"].replace(999, np.nan)
df = df.drop(columns=["pdays", "duration"])

print(df.shape)
print(df.columns.tolist())

# now split x and y
X = df.drop(columns=["y"])
y = df["y"]

# print("X shape:", X.shape)
# print("y shape:", y.shape)
#
# print("\nX columns:")
# print(X.columns.tolist())
#
# print("\ny values:")
# print(y.value_counts()) # gives count of no and yes in y col

# print(X.dtypes)

# split the data into test and train

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2, # tells 20% test size
    random_state=42, # this will give fixed set each time without this code will give diff y_Test each time
    stratify=y # this helps to preserve the distribution in y_test and y_train as original y
)

# print("X_train:", X_train.shape)
# print("X_test :", X_test.shape)
#
# print("\ny_train distribution:")
# print(y_train.value_counts(normalize=True)) # normalize will give values with percentage rather than just counts
#
# print("\ny_test distribution:")
# print(y_test.value_counts(normalize=True))

categorical_columns = X_train.select_dtypes(include="object").columns

# encoder helps to create cols for each value possible for that obj like following for job
# 'job_admin.' 'job_blue-collar' 'job_entrepreneur' 'job_housemaid'
#  'job_management' 'job_retired' 'job_self-employed' 'job_services'
#  'job_student' 'job_technician' 'job_unemployed' 'job_unknown'
encoder = OneHotEncoder(
    handle_unknown="ignore", # this will hlp to avoid error it test has some unknown category from train
    sparse_output=False # there is sparse matrix generation and we dont want it rn
)

encoder.fit(X_train[categorical_columns])

X_train_encoded = encoder.transform(X_train[categorical_columns])
X_test_encoded = encoder.transform(X_test[categorical_columns])

# print("Encoded train shape:", X_train_encoded.shape)

encoded_feature_names = encoder.get_feature_names_out(categorical_columns)

# print("\nEncoded features:")
# print(encoded_feature_names)

# print("\nNumber of encoded features:", len(encoded_feature_names))

# working on other columns now...
numerical_cols = X_train.select_dtypes(exclude="object").columns
# print("Numerical columns:")
# print(numerical_cols)

# extract numeric data
X_train_numeric = X_train[numerical_cols]
X_test_numeric = X_test[numerical_cols]

# print(X_train_numeric.shape)
# print(X_test_numeric.shape)

# now we create combined numeric and encoded cols (hstack is kinda horizontal stack)
# creates one final feature matrix
X_train_final = np.hstack([X_train_numeric, X_train_encoded])
X_test_final = np.hstack([X_test_numeric, X_test_encoded])

print(X_train_final.shape)
print(X_test_final.shape)

print(df["days_since_contact"])