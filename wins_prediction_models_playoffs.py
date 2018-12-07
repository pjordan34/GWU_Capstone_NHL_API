import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB

"""" For all of the models I choose to go with the shootouts included as they gave a better representation of wins. additionally 
you will find that I have dropped several columns that were either Goals or were derived using goals. I did keep shooting% and it likely contributes 
to the accuracy of the model. 

"""
# read in data and get it into X, y format. I also made sure all data was in the proper type

df = pd.read_csv('data/2014agg_playoffs.csv', dtype={'Goals_for': int})
df.dropna(inplace=True)
df = pd.get_dummies(df, drop_first=True)
# df.info()
y = df['Win'].values
X = df.drop(['Win', 'Season', 'Goals_for', 'Goals_A', 'Goals_for%', 'Sv%', 'wshF%', 'wshF', 'wshA'], axis=1).values
# set up training and test data. will have to do this again for 2018(as there is an additional team)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# read in the rest of the seasons
df2015 = pd.read_csv('data/2015agg_playoffs.csv',
                     dtype={'Misses': int, 'SOG_for': int, 'Hits_for': int, 'Goals_for': int, 'Fenwick_for': int})
df2015.dropna(inplace=True)
df2015 = df2015.set_index(['Ev_Team'])
# get rid of the extra row
df2015.drop(['#'], inplace=True)
df2015 = df2015.reset_index()
df2015 = pd.get_dummies(df2015, drop_first=True)
# df2015.info()
y_2015 = df2015['Win'].values
X_2015 = df2015.drop(['Win', 'Season', 'Goals_for', 'Goals_A', 'Goals_for%', 'Sv%', 'wshF%', 'wshF', 'wshA'],
                     axis=1).values

df2016 = pd.read_csv('data/2016agg_playoffs.csv', dtype={'Goals_for': int})
df2016.dropna(inplace=True)
df2016 = pd.get_dummies(df2016, drop_first=True)
# df.info()
y_2016 = df2016['Win'].values
X_2016 = df2016.drop(['Win', 'Season', 'Goals_for', 'Goals_A', 'Goals_for%', 'Sv%', 'wshF%', 'wshF', 'wshA'],
                     axis=1).values

df2017 = pd.read_csv('data/2017agg_playoffs.csv', dtype={'Misses': int, 'Goals_for': int, 'Fenwick_for': int})
df2017.dropna(inplace=True)
df2017 = pd.get_dummies(df2017, drop_first=True)
# df2017.info()
y_2017 = df2017['Win'].values
X_2017 = df2017.drop(['Win', 'Season', 'Goals_for', 'Goals_A', 'Goals_for%', 'Sv%', 'wshF%', 'wshF', 'wshA'],
                     axis=1).values

df2018 = pd.read_csv('data/2018agg_playoffs.csv', dtype={'Goals_for': int})
df2018.dropna(inplace=True)
df2018 = pd.get_dummies(df2018, drop_first=True)
# df2018.info()
y_2018 = df2018['Win'].values
X_2018 = df2018.drop(['Win', 'Season', 'Goals_for', 'Goals_A', 'Goals_for%', 'Sv%', 'wshF%', 'wshF', 'wshA'],
                     axis=1).values
X_2018train, X_2018test, y_2018train, y_2018test = train_test_split(X_2018, y_2018, test_size=0.3, random_state=42)


"""""first we will run a naive bayes tree and see how well it predicts wins based on the aggregated data 
I'll run it with the 2014 data train/test, then run up through the 2017season, we will train a second model on 2018 and 
do a final test on the current season
"""""
bayes = GaussianNB()
bayes.fit(X_train, y_train)

y_pred = bayes.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
y_pred2015 = bayes.predict(X_2015)
print(confusion_matrix(y_2015, y_pred2015))
print(classification_report(y_2015, y_pred2015))
y_pred2016 = bayes.predict(X_2016)
print(confusion_matrix(y_2016, y_pred2016))
print(classification_report(y_2016, y_pred2016))
y_pred2017 = bayes.predict(X_2017)
print(confusion_matrix(y_2017, y_pred2017))
print(classification_report(y_2017, y_pred2017))

"""" Next we will train/test 2018 and test on 2019. we have to do this because the NHL added the Vegas team in 2018
so the data is shaped differently. 
"""""
bayes2 = GaussianNB()
bayes2.fit(X_2018train, y_2018train)

y_pred2018 = bayes2.predict(X_2018test)
print(confusion_matrix(y_2018test, y_pred2018))
print(classification_report(y_2018test, y_pred2018))



""""" Now to try a Logistic Regression with cross-validation for 2014-2017
"""""

c_space = np.logspace(-5, 8, 15)
param_grid = {'C': c_space, 'penalty': ['l1', 'l2']}

logReg = LogisticRegression()
logReg_cv = GridSearchCV(logReg, param_grid, cv=5)

best_model = logReg_cv.fit(X_train, y_train)

print("Tuned Logistic Regression Parameter: {}".format(best_model.best_params_))
print("Tuned Logistic Regression Accuracy: {}".format(best_model.best_score_))

y_pred = best_model.predict(X_test)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

y_pred_prob = best_model.predict_proba(X_test)[:, 1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.savefig('data/ROC_Curve_playoffs_2014')
# plt.show()
plt.clf()
print("AUC: {}".format(roc_auc_score(y_test, y_pred_prob)))

y_pred2015 = best_model.predict(X_2015)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_2015, y_pred2015))
print(classification_report(y_2015, y_pred2015))

y_pred_prob2015 = best_model.predict_proba(X_2015)[:, 1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_2015, y_pred_prob2015)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.savefig('data/ROC_Curve_playoffs_2015')
# plt.show()
plt.clf()
print("AUC: {}".format(roc_auc_score(y_2015, y_pred_prob2015)))

y_pred2016 = best_model.predict(X_2016)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_2016, y_pred2016))
print(classification_report(y_2016, y_pred2016))

y_pred_prob2016 = best_model.predict_proba(X_2016)[:, 1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_2016, y_pred_prob2016)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.savefig('data/ROC_Curve_playoffs_2016')
# plt.show()
plt.clf()
print("AUC: {}".format(roc_auc_score(y_2016, y_pred_prob2016)))

y_pred2017 = best_model.predict(X_2017)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_2017, y_pred2017))
print(classification_report(y_2017, y_pred2017))

y_pred_prob2017 = best_model.predict_proba(X_2017)[:, 1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_2017, y_pred_prob2017)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.savefig('data/ROC_Curve_playoffs_2017')
# plt.show()
plt.clf()
print("AUC: {}".format(roc_auc_score(y_2017, y_pred_prob2017)))

""" Now to do the 2018 and 2019 data

"""

best_model2 = logReg_cv.fit(X_2018train, y_2018train)

print("Tuned Logistic Regression Parameter: {}".format(best_model2.best_params_))
print("Tuned Logistic Regression Accuracy: {}".format(best_model2.best_score_))

y_pred2018 = best_model2.predict(X_2018test)

# Compute and print the confusion matrix and classification report
print(confusion_matrix(y_2018test, y_pred2018))
print(classification_report(y_2018test, y_pred2018))

y_pred_prob2018 = best_model2.predict_proba(X_2018test)[:, 1]

# Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_2018test, y_pred_prob2018)

# Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.savefig('data/ROC_Curve_playoffs_2018')
# plt.show()
plt.clf()
print("AUC: {}".format(roc_auc_score(y_2018test, y_pred_prob2018)))


