# -*- coding: utf-8 -*-
"""Final Version CI-HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hiDBDSY5W-Lg4YTiaeuChMYrzrKHLN1t
"""

import csv
  import numpy as np
  import pandas as pd
  from pandas.api.types import CategoricalDtype 
  from sklearn.model_selection import train_test_split
  import ast
  from collections import Counter 
  from sklearn.svm import SVC
  from math import sqrt
  import time

def keel_to_csv():
  all_categories_attr = {}
  with open("adult.csv", "w") as cf:
    writer = csv.writer(cf)
    with open("adult.dat", "r") as df:
      lines = df.readlines()
      for line in range(1,16):
        attr_subject = lines[line][10:].split(' ', 2)[1]
        attr_data = lines[line][10:].split(' ', 2)[2][:-1]

        if not attr_data.startswith("real "):
            all_categories_attr[attr_subject] =  attr_data.strip('}{').split(', ')
    
      attr = lines[16][8:-1].split(', ')
      attr_out = lines[17][9:-1]
      attr.append(attr_out)
      writer.writerow(attr)
      for line in lines[19:]:
        all_data = line.split(',')
        true_data = all_data[:-1]
        true_data.append(all_data[-1][:-1])
        writer.writerow(true_data)

  return all_categories_attr

def read_csv(all_categories_attr):

  csv_file_name = 'adult.csv'
  csv_file = pd.read_csv(csv_file_name)

  age = csv_file['Age'].values
  workclass = csv_file['Workclass'].values
  fnlwgt = csv_file['Fnlwgt'].values
  education = csv_file['Education'].values
  education_num = csv_file['Education-num'].values
  marital_status = csv_file['Marital-status'].values
  occupation = csv_file['Occupation'].values
  relationship = csv_file['Relationship'].values
  race = csv_file['Race'].values
  sex = csv_file['Sex'].values
  capital_gain = csv_file['Capital-gain'].values
  capital_loss = csv_file['Capital-loss'].values
  hours_per_week = csv_file['Hours-per-week'].values
  native_country = csv_file['Native-country'].values
  result = csv_file['Class'].values

  columns_names = ['Age', 'Workclass', 'Fnlwgt', 'Education', 'Education-num', 'Marital-status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Capital-gain', 'Capital-loss', 'Hours-per-week', 'Native-country', 'Class']
  df = pd.DataFrame(list(zip(age, workclass, fnlwgt, education, education_num, marital_status, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, result)), columns = columns_names)

  for column in df.columns:
    if df[column].dtypes == "object":
      df[column].replace({"?": df[column].value_counts().idxmax()}, inplace=True)
      if column in list(all_categories_attr.keys()):
        if column != "Sex" and column != "Class":
          df[column] = df[column].astype(CategoricalDtype(all_categories_attr[column]))
          df = df.join(pd.get_dummies(df[column],prefix=column))
          df = df.drop(column,axis = 1)
      else:
        df[column] = df[column].astype(int)
    else:
      pass

  df["Sex"].replace({"Female": 0, "Male" : 1}, inplace=True)
  df["Class"].replace({"<=50K": 0, ">50K" : 1}, inplace=True)

  normalized_df = (df - df.min()) / (df.max() - df.min())

  X = normalized_df.drop("Class",axis = 1)
  X = X.to_numpy()
  Y = normalized_df["Class"]
  Y = Y.to_numpy()

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.01, random_state=0)

  print(df)

  print("\nData Info:")
  print("DataSet Size: " + str(len(df)))
  print("Training Data Size: " + str(len(X_train)))
  print("Testing Data Size: " + str(len(X_test)))


  return X_train, X_test, Y_train, Y_test, df.min(), df.max()

def euclidean_distance(first, second):
  return np.sqrt(np.sum(np.power((second - first),2), axis = 1))

def knn(trains, tests, out_trains, out_tests, k):
  print("=================================")
  print("Processing Manual KNN for K = " + str(k))

  start_time = time.time()

  true_predict = 0   

  for test in range(len(tests)):
    dis = np.empty(0)
    dis = np.append(dis, euclidean_distance(tests[test], trains))

    index = np.argsort(dis)[0:k]

    dis = np.sort(dis)[0:k]

    decision = np.empty(0)

    for i in index:
      decision = np.append(decision, out_trains[i])

    final_decision = Counter(decision).most_common(1)[0][0] 
 
    if out_tests[test] == final_decision:
        true_predict += 1
    # break

  end_time = time.time()

  accuracy = true_predict / len(out_tests) * 100
  print("Finished! in " +str(end_time - start_time)+ "s\nAccuracy of Manual KNN:" + str(accuracy))

def svm(X_train, X_test, Y_train, Y_test):
  
  print("=================================")
  print("Processing SKLearn SVM")
  
  start_time = time.time()


  svclassifier = SVC(kernel='linear')
  svclassifier.fit(X_train, Y_train)
  Y_predict = svclassifier.predict(X_test)

  end_time = time.time()

  accuracy = (len(Y_test) - np.count_nonzero(Y_test - Y_predict)) / len(Y_test) *100

  print("Finished! in " +str(end_time - start_time) + "s\nAccuracy of SKLearn SVM:" + str(accuracy))

from sklearn.neighbors import KNeighborsClassifier
def knn_skilearn(X_train, X_test, Y_train, Y_test, k):
  
  print("=================================")
  print("Processing SKLearn KNN for K = " + str(k))

  start_time = time.time()

  classifier = KNeighborsClassifier(n_neighbors=k)
  classifier.fit(X_train, Y_train)
  Y_predict = classifier.predict(X_test)

  end_time = time.time()

  accuracy = (len(Y_test) - np.count_nonzero(Y_test - Y_predict)) / len(Y_test) *100

  print("Finished! in " +str(end_time - start_time)+ "s\nAccuracy of SKLearn KNN:" + str(accuracy))

def main():
  all_categories_attr = keel_to_csv()
  X_train, X_test, Y_train, Y_test, min, max = read_csv(all_categories_attr)
  k_init = int(sqrt(len(Y_test)))
  k = int(input("\nK has been set to " + str(k_init) + "\nWanna change it?\n-1=no\nEnter Number for K: "))
  if k == -1:
    k = k_init
  knn(X_train, X_test,Y_train, Y_test, k)
  knn_skilearn(X_train, X_test,Y_train, Y_test, k)
  svm(X_train, X_test, Y_train, Y_test)

if __name__ == "__main__":
  main()