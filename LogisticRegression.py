# -*- coding: utf-8 -*-
"""STT0AH_Indah Reski.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kKllaFK23pj3HT_NaNd2PYoviIpWQ1q4

# **Classification Analysis Using the Logistic Regression Method**

> **Table of Contents:**


1.   Data preprocessing
2.   Descriptive analysis
3.   Encode categorical variables
4.   Feature selection
5.   Splitting data into training and testing
6.   Handling unbalanced data using SMOTE
7.   Feature scalling
8.   Model training
9.   Predict result
10.  Accuracy score
11.  Confusion matrix
12.  Predict test data using model based on traning set

## **Data Preprocessing**
"""

# Commented out IPython magic to ensure Python compatibility.
# Import libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # for data visualization
import seaborn as sns # for statistical data visualization
# %matplotlib inline

# Import data training
tr = pd.read_csv("/content/Churn_train.csv") #train
tr.head()

# view summary of dataset

tr.info()

"""We can see that there are no missing values ​​in the dataset and it seems that there are variables with object data types.

To ensure that our data is completely clean and ready for analysis, we will look for missing values ​​in the dataset.
"""

# check for missing values in variables

tr.isnull().sum()

"""We can see that there are no missing values in the dataset.

## **Descriptive Analysis**

Now we will explore the data with descriptive analysis to gain insights into the dataset used.
"""

# view dimensions of dataset

tr.shape

"""We can see that there are 9,114 instances and 21 attributes in our dataset."""

# correlation matrix

tr.corr()

corrMatrix = tr.corr()
sns.heatmap(corrMatrix, annot=False)
plt.show()

"""As we know earlier, the 'Churn_Flag' attribute can be used as the class label/target. So we will check the distribution on the class label."""

# check distribution of class column

tr['Churn_Flag'].value_counts()

sns.countplot(x='Churn_Flag', data=tr, palette='hls')
plt.show()
plt.savefig('count_plot')

# view the percentage distribution of class column

pct = tr['Churn_Flag'].value_counts()/np.float(len(tr))

print("percentage of negative class is", pct[0]*100)
print("percentage of positive class is", pct[1]*100)

"""Of the 9,114 instances in the dataset, 83.9% (7,650) were negative class samples, and the rest 16.06% (1,464) were positive class samples."""

tr.groupby('Churn_Flag').mean()

# find categorical variables

categorical = [var for var in tr.columns if tr[var].dtype=='O']

print('There are {} categorical variables\n'.format(len(categorical)))
print('The categorical variables are :', categorical)

tr.groupby('Gender').mean()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
pd.crosstab(tr.Gender,tr.Churn_Flag).plot(kind='bar')
plt.title('Customer Frequency for Gender')
plt.xlabel('Gender')
plt.ylabel('Frequency of Customers')
plt.savefig('customer_gender')

tr.groupby('Education_Level').mean()

table=pd.crosstab(tr.Education_Level,tr.Churn_Flag)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Education Level')
plt.xlabel('Education Level')
plt.ylabel('Proportion of Customers')
plt.savefig('edu_stack')

tr.groupby('Marital_Status').mean()

table=pd.crosstab(tr.Marital_Status,tr.Churn_Flag)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Marital Status')
plt.xlabel('Marital Status')
plt.ylabel('Proportion of Customers')
plt.savefig('mar_stack')

tr.groupby('Income_Category').mean()

table=pd.crosstab(tr.Income_Category,tr.Churn_Flag)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Income Category')
plt.xlabel('Income Category')
plt.ylabel('Proportion of Customers')
plt.savefig('inc_stack')

tr.groupby('Card_Category').mean()

table=pd.crosstab(tr.Card_Category,tr.Churn_Flag)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Card Category')
plt.xlabel('Card Category')
plt.ylabel('Proportion of Customers')
plt.savefig('card_stack')

# view summary statistics in numerical variables

round(tr.describe(),2)

"""## **Encode Categorical Variables**

We will convert the string value to a type integer by using Label Encoder in the scikit-learn library.
"""

# Converting string value to int type

from sklearn.preprocessing import LabelEncoder

tr['Gender'] = LabelEncoder().fit_transform(tr['Gender'])
tr['Education_Level'] = LabelEncoder().fit_transform(tr['Education_Level'])
tr['Marital_Status'] = LabelEncoder().fit_transform(tr['Marital_Status'])
tr['Income_Category'] = LabelEncoder().fit_transform(tr['Income_Category'])
tr['Card_Category'] = LabelEncoder().fit_transform(tr['Card_Category'])

"""## **Feature Selection**

**The Recursive Feature Elimination** (or RFE) works by recursively removing attributes and building a model on those attributes that remain. It uses the model accuracy to identify which attributes (and combination of attributes) contribute the most to predicting the target attribute.
"""

# Feature Extraction with RFE
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# load data
X = tr.loc[:, tr.columns != 'Churn_Flag']
Y = tr.loc[:, tr.columns == 'Churn_Flag']

# feature extraction
model = LogisticRegression(solver='lbfgs')
rfe = RFE(model, step=5)
fit = rfe.fit(X, Y)

print("Num Features: %d" % fit.n_features_)
print("Selected Features: %s" % fit.support_)
print("Feature Ranking: %s" % fit.ranking_)

"""**Selected Features:**

`['Customer_Age', 'Education_Level', 'Months_on_book',
      'Total_Relationship_Count', 'Credit_Limit', 'Total_Revolving_Bal',
      'Avg_Open_To_Buy', 'Total_Trans_Amt', 'Total_Trans_Ct']`

"""

cols = ['Customer_Age', 'Education_Level', 'Months_on_book',
      'Total_Relationship_Count', 'Credit_Limit', 'Total_Revolving_Bal',
      'Avg_Open_To_Buy', 'Total_Trans_Amt', 'Total_Trans_Ct', 'Churn_Flag']

df = tr.loc[:, ~tr.columns.isin(cols)]
tr.drop(columns=df, inplace=True)

tr.head()

"""## **Splitting Data Into Separate Training and Testing**

Splitting dataset into training set and testing set for better generalization.
"""

# split X and y into training and testing sets

from sklearn.model_selection import train_test_split

X = tr.loc[:, tr.columns != 'Churn_Flag']
y = tr.loc[:, tr.columns == 'Churn_Flag']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""## **Handling Unbalanced Data Using SMOTE**

**SMOTE (synthetic minority oversampling technique)** is one of the most commonly used oversampling methods to solve the imbalance problem.
It aims to balance class distribution by randomly increasing minority class examples by replicating them.
"""

from imblearn.over_sampling import SMOTE
os = SMOTE(random_state=0)

columns = X_train.columns
os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['Churn_Flag'])

# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of no subscription in oversampled data",len(os_data_y[os_data_y['Churn_Flag']==0]))
print("Number of subscription",len(os_data_y[os_data_y['Churn_Flag']==1]))
print("Proportion of no subscription data in oversampled data is ",len(os_data_y[os_data_y['Churn_Flag']==0])/len(os_data_X))
print("Proportion of subscription data in oversampled data is ",len(os_data_y[os_data_y['Churn_Flag']==1])/len(os_data_X))

"""## **Feature Scaling**

**Data standardization.** Standardization of datasets is a common requirement for many machine learning estimators implemented in scikit-learn; they might behave badly if the individual features do not more or less look like standard normally distributed data.
"""

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)

X_train = pd.DataFrame(X_train, columns = columns)
X_train.head()

"""## **Model Training**"""

# train a logistic regression model on the training set
from sklearn.linear_model import LogisticRegression

# instantiate the model
logreg = LogisticRegression(solver='liblinear', random_state=0)

# fit the model
logreg.fit(X_train, y_train)

"""## **Predict Result**"""

y_pred_test = logreg.predict(X_test)
y_pred_test

"""## **Accuracy Score**"""

from sklearn.metrics import accuracy_score

print('Model accuracy score: {0:0.4f}'. format(accuracy_score(y_test, y_pred_test)))

# Compare the training-set and testing-set accuracy

y_pred_train = logreg.predict(X_train)
print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train)))

# Check underfitting and overfitting

# print the scores on training and test set
print('Training set score: {:.4f}'.format(logreg.score(X_train, y_train)))
print('Test set score: {:.4f}'.format(logreg.score(X_test, y_test)))

"""**Change the parameter from C=1 into smaller C=0.1**"""

# fit the Logsitic Regression model with C=0.1

# instantiate the model
logreg_C = LogisticRegression(C=0.1, solver='liblinear', random_state=0)

# fit the model
logreg_C.fit(X_train, y_train)

# print the scores on training and test set

print('Training set score: {:.4f}'.format(logreg_C.score(X_train, y_train)))

print('Test set score: {:.4f}'.format(logreg_C.score(X_test, y_test)))

"""Produces a better level of accuracy by using a smaller C parameter of 0.1"""

y_pred_test_C = logreg_C.predict(X_test)
y_pred_test_C

"""## **Confusion Matrix**"""

# Print the Confusion Matrix and slice it into four pieces

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred_test_C)

print('Confusion matrix\n\n', cm)
print('\nTrue Positives(TP) = ', cm[0,0])
print('\nTrue Negatives(TN) = ', cm[1,1])
print('\nFalse Positives(FP) = ', cm[0,1])
print('\nFalse Negatives(FN) = ', cm[1,0])

# visualize confusion matrix with seaborn heatmap

cm_matrix = pd.DataFrame(data=cm, columns=['Actual Positive:1', 'Actual Negative:0'], 
                                 index=['Predict Positive:1', 'Predict Negative:0'])

sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='YlGnBu')

"""**Classification Report**"""

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred_test_C))

"""**Classification Accuracy**"""

TP = cm[0,0]
TN = cm[1,1]
FP = cm[0,1]
FN = cm[1,0]

# print classification accuracy

classification_accuracy = (TP + TN) / float(TP + TN + FP + FN)

print('Classification accuracy : {0:0.4f}'.format(classification_accuracy))

"""## **Predict test data using model based on traning set**

**Import data testing**
"""

# Import data testing
ts = pd.read_csv("/content/Churn_test.csv") #test
ts = pd.DataFrame(ts)
ts.head()

ts.info()

cols = ['Customer_Age', 'Education_Level', 'Months_on_book',
      'Total_Relationship_Count', 'Credit_Limit', 'Total_Revolving_Bal',
      'Avg_Open_To_Buy', 'Total_Trans_Amt', 'Total_Trans_Ct']

dft = ts.loc[:, ~ts.columns.isin(cols)]
ts.drop(columns=dft, inplace=True)

ts.head()

# Converting string value to int type

from sklearn.preprocessing import LabelEncoder

ts['Gender'] = LabelEncoder().fit_transform(ts['Gender'])
ts['Education_Level'] = LabelEncoder().fit_transform(ts['Education_Level'])
ts['Marital_Status'] = LabelEncoder().fit_transform(ts['Marital_Status'])
ts['Income_Category'] = LabelEncoder().fit_transform(ts['Income_Category'])
ts['Card_Category'] = LabelEncoder().fit_transform(ts['Card_Category'])

columns = ts.columns

"""**Feature Scalling**"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
ts = scaler.fit_transform(ts)

ts = pd.DataFrame(ts, columns=columns)
ts.head()

"""**Fitting Model**"""

#factors that will predict the churn
desired_factors = ['Customer_Age', 'Education_Level', 'Months_on_book',
      'Total_Relationship_Count', 'Credit_Limit', 'Total_Revolving_Bal',
      'Avg_Open_To_Buy', 'Total_Trans_Amt', 'Total_Trans_Ct']

#set prediction data to factors that will predict, and set target
train_data = tr[desired_factors]
test_data = ts[desired_factors]
target = tr.Churn_Flag

#fitting model with prediction data and telling it my target
logreg_C.fit(train_data, target)
logreg_C.predict(test_data.head())

"""**Create csv file**"""

predictions = logreg_C.predict(test_data)
                           
submit_df = pd.DataFrame()
submit_df['CLIENTNUM'] = ts['CLIENTNUM']
submit_df['Churn_Flag'] = predictions
submit_df.to_csv('churn_test.csv', index= False)

"""## **References**

https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

https://www.kaggle.com/code/prashant111/logistic-regression-classifier-tutorial/notebook
"""