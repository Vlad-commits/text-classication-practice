import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Create data
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm

import dataframe_provider

df = dataframe_provider.get_dataframe()

columns = ["letters_count", "total_punctuation_signs"]

X = df[columns].to_numpy()

y  = df["author_label"].to_numpy()

X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X[y == 1], y[y == 1], test_size=0.33, random_state=42)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X[y == -1], y[y == -1], test_size=0.33, random_state=42)

X_train = np.concatenate((X_train_1, X_train_2), axis=0)
X_test = np.concatenate((X_test_1, X_test_2), axis=0)
y_train = np.concatenate((y_train_1, y_train_2), axis=0)
y_test = np.concatenate((y_test_1, y_test_2), axis=0)

clf = svm.SVC(C=1.0, kernel='linear')
# scores = cross_val_score(clf, X, y, cv=5)

clf.fit(X_train, y_train)
print(clf.coef0)
print(clf.dual_coef_)

print(classification_report(y_test, clf.predict(X_test)))
print(classification_report(y_train, clf.predict(X_train)))
