import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc("font", size=14)
sns.set(style="ticks", color_codes=True)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from collections import Counter
from skater.model import InMemoryModel
from skater.core.explanations import Interpretation
import cleaning as cln

def country_disaggregate(df):
    india_mask = df['geo_level_1'] == "India"
    df_india = df[india_mask]
    malawi_mask = df['geo_level_1'] == "Malawi"
    df_malawi = df[malawi_mask]
    rwanda_mask = df['geo_level_1'] == "Rwanda"
    df_rwanda = df[rwanda_mask]
    uganda_mask = df['geo_level_1'] == "Uganda"
    df_uganda = df[uganda_mask]
    # df_india shape: (5991, 17)
    # df_malawi shape: (1730, 17)
    # df_rwanda shape: (743, 17)
    # df_uganda.shape: (1567, 17)
    return df_india, df_malawi, df_rwanda, df_uganda


def dummify(df, categoricals, additional_drops, final_drops):
    # Leaving in categorical columns and "one hot" dummy column for use in EDA
    dummies = pd.get_dummies(df[categoricals])
    full_dummied = pd.concat((dummies, df), axis=1)
    # The following technology only exists in Malawi and should only be included in Malawi specifc analysis
    full_dummied.drop(additional_drops, axis=1, inplace=True)
    full_dummied.drop(final_drops, axis=1, inplace=True)
    return full_dummied


def split(dataframe, categoricals, one_hot_features):
    y = dataframe.pop('water_available_from_point_on_day_of_visit')
    X = dataframe
    drop_columns = categoricals
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=21)
    remove_cats_and_one_hot = [X_train, X_test]
    df_eda = pd.concat((X_train, y_train), axis=1)
    for i in one_hot_features:
        drop_columns.append(i)
    for i in remove_cats_and_one_hot:
        i.drop(drop_columns, axis=1, inplace=True)
    return df_eda, X_train, X_test, y_train, y_test


def upsample(X, y):
    sm = SMOTE(random_state=32, k_neighbors=4, ratio=1.0)
    X_smote, y_smote = sm.fit_sample(X, y)
    return X_smote, y_smote


def kfold_train_precision(model, X, y):
    k_fold = KFold(n_splits=4)
    scores = []
    manual_score = []
    for train_idx, test_idx in k_fold.split(X, y):
        model.fit(X[train_idx], y[train_idx])
        y_predict = model.predict(X[test_idx])
        scores.append(precision_score(y[test_idx], y_predict))
    return np.average(scores)


def eda(df_eda):
    '''run initial eda on the data frame before train-test split, but after
    removing the hold out set'''
    pass


def select_rand_forest(X_train, y_train):
    estimators = [50]
    best_precision = 0.0001
    for i in estimators:
        forest = RandomForestClassifier(n_estimators=i, class_weight='balanced')
        precision = kfold_train_precision(forest, X_train, y_train)
        if precision > best_precision:
            best_precision = precision
            best_estimator = i
        print("Precision with", i, "estimators: ", round(precision, 3))
    return best_estimator, forest


def rand_forest(X_train, X_holdout, y_train, y_holdout, model, estimator):
    model.fit(X_train, y_train)
    y_predict = forest.predict(X_holdout)
    score = precision_score(y_holdout, y_predict)
    tn, fp, fn, tp = confusion_matrix(y_holdout, y_predict).ravel()
    print("Precision score with holdout data: ", round(score, 3))
    return forest, score


def feat_imps(model, X_train, y_train):
    model.fit(X_train, y_train)
    return forest.feature_importances_


if __name__ == "__main__":
    data = pd.read_csv('wfp_pumps.csv')
    df = cln.clean(data)
    interpreter = Interpretation()
    df_india, df_malawi, df_rwanda, df_uganda = country_disaggregate(df)
    categoricals = ['geo_level_1', 'water_point_type']
    one_hot_features = ['geo_level_1_India', 'water_point_type_Phe 6 Handpump']
    additional_drops = ['water_point_type_Afridev Handpump', 'adequate_water_quality', 'water_point_type_Afridev Handpump']
    final_drops = ['spring_protection_past_lifespan', 'water_point_type_Protected Deep Borehole', 'geo_level_1_Rwanda', 'apron_past_lifespan', 'taps_past_lifespan']
    full_dummied = dummify(df, categoricals, additional_drops, final_drops)
    df_eda, X_train, X_test, y_train, y_test = split(full_dummied, categoricals, one_hot_features)
    X_smote, y_smote = upsample(X_train, y_train)
    estimator, forest = select_rand_forest(X_smote, y_smote)
    forest, score = rand_forest(X_smote, X_test, y_smote, y_test, forest, estimator)
    feat_importances = feat_imps(forest, X_train, y_train)
