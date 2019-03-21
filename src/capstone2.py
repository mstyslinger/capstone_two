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
from collections import Counter


def clean(data):
    drop_cols = ['geo_level_7', 'geo_level_6', 'geo_level_5', 'geo_level_4', 'geo_level_3', 'geo_level_2', 'components', 'data_collection_year','water_point_id', 'alert', 'risk_based_on_age', 'risk_based_on_current_condition', 'level_of_priority_to_repair_or_replace', 'recommended_activity', 'state_of_spring_protection', 'state_of_taps', 'state_of_well', 'state_of_pump', 'state_of_apron', 'out_of_service_one_day_or_less_in_past_month', 'presense_of_spring_protection', 'water_point_in_good_overall_condition', 'year_spring_protection_constructed_or_reconstructed', 'presense_of_tap', 'year_taps_constructed_or_reconstructed', 'presense_of_well', 'year_well_constructed_or_reconstructed', 'presense_of_pump', 'year_pump_constructed_or_reconstructed', 'presense_of_apron', 'year_apron_constructed_or_reconstructed', 'days_out_of_service_in_last_year', 'level_of_service', 'level_of_service_score', 'families_with_access_to_improved_water', 'families_without_access_to_improved_water', 'overall_state_of_water_point']
    # Geo level 7 had 7,505 NaN values, geo level 6 had 2,478, and components has 5751
    # Geo level 2: India only has 2 states in the dataset and Rwanda, Uganda, and Malawi each only have 1
    # Geo level 3 - 5: The dataframes are too small for meaningful prediction when disaggregated down to this level
    # Families with access to imporved water was exactly the same as num_families_in_community, and families w/out access showed no corelation
    # Others dropped for incompatability to the analysis
    df = data.drop(drop_cols, axis=1)
    df.dropna(inplace=True)
    # resulting dataframe shape after remaining NaNs are dropped: (10033, 23)
    df = df.rename(columns={"remaining_lifespan_of_spring_protection":"spring_protection_past_lifespan", "remaining_lifespan_of_taps":"taps_past_lifespan", "remaining_lifespan_of_well":"well_past_lifespan", "remaining_lifespan_of_pump":"pump_past_lifespan", "remaining_lifespan_of_apron":"apron_past_lifespan"})
    # Replace blank values with 0:
    blanks = ['spring_protection_past_lifespan', 'taps_past_lifespan','well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan']
    for i in blanks:
        df[i].replace(" ", "0", inplace=True)
    # replace water point technologies having less than 150 entries with "other"
    other_technologies  = ['Pond', 'Unprotected Spring', 'Tara Direct Action Pump', 'Malda Handpump', 'Unprotected Well', 'River/Stream', 'Stream', 'Scoophole', 'Mark Iii Handpump', 'Solar Powered Borehole', 'River', 'Unprotected Shallow Well', 'Elephant Pump', 'Mark Iv Handpump', 'Sabmisable Pump', 'Canal', 'Artisan Well', 'Borehole', 'Climax']
    for i in other_technologies:
        df['water_point_type'].replace(i, "other", inplace=True)
    # Delete extra space after Uganda in geo_level_1 feature:
    df['geo_level_1'].replace('Uganda ', 'Uganda', inplace=True)
    # Other replacement:
    df['spring_protection_past_lifespan'].replace("#VALUE!", "0", inplace=True)
    df['age_since_original_construction'].replace(" ", "2017", inplace=True)
    # Change string numbers to numeric values:
    numeric = ['num_families_in_community', 'age_since_original_construction', 'spring_protection_past_lifespan', 'taps_past_lifespan', 'well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan']
    for i in numeric:
        df[i] = pd.to_numeric(df[i])
    # Transform years to ages:
    df['age_since_original_construction'] = df['age_since_original_construction'].apply(lambda x: 2017 - x)
    # Drop outlier values (typo entries):
    outlier_mask = (df['age_since_original_construction'] < 150) & (df['age_since_original_construction'] >= 0)
    df = df[outlier_mask]
    # Transform component lifespans to categorical values (1= older than lifespan, 0= within lifespan or non-existent):
    lifespans = ['spring_protection_past_lifespan', 'taps_past_lifespan','well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan']
    lifespan_mask = df[lifespans] < 0
    df[lifespans] = (lifespan_mask*1).astype(int)
    # dF shape (10031, 17)
    return df


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


def dummify(df, categoricals):
    # Leaving in categorical columns and "one hot" dummy column for use in EDA
    dummies = pd.get_dummies(df[categoricals])
    full_dummied = pd.concat((dummies, df), axis=1)
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
    sm = SMOTE(random_state=21, ratio=1.0)
    X_smote, y_smote = sm.fit_sample(X, y)
    return X_smote, y_smote

def kfold_train_precision(model, X, y):
    k_fold = KFold(n_splits=5)
    scores = []
    tn_rate = []
    fp_rate = []
    fn_rate = []
    tp_rate = []
    for train_idx, test_idx in k_fold.split(X, y):
        model.fit(X[train_idx], y[train_idx])
        y_predict = model.predict(X[test_idx])
        tn, fp, fn, tp = confusion_matrix(y[test_idx], y_predict).ravel()
        scores.append(precision_score(y[test_idx], y_predict))
        tn_rate.append(tn/len(y[test_idx]))
        fp_rate.append(fp/len(y[test_idx]))
        fn_rate.append(fn/len(y[test_idx]))
        tp_rate.append(tp/len(y[test_idx]))
    return round(np.average(scores), 3), round(np.average(tn_rate), 3), round(np.average(fp_rate), 3), round(np.average(fn_rate), 3), round(np.average(tp_rate), 3)


def eda(df_eda):
    '''run initial eda on the data frame before train-test split, but after
    removing the hold out set'''
    pass


def select_rand_forest(X_train, y_train):
    estimators = [2, 10, 25, 50, 100, 1000]
    best_precision = 0.001
    for i in estimators:
        forest = RandomForestClassifier(n_estimators=i, class_weight='balanced')
        precision, tn, fp, fn, tp = kfold_train_precision(forest, X_train, y_train)
        if precision > best_precision:
            best_precision = precision
            best_estimator = i
        # Sklearn precision score:
        print("Precision with", i, "estimators: ", precision)
        # Manual precision score:
        print("Precision (manual) with", i, "estimators: ", round(tp/(tp+fp),3))
        print('True negative | False positive')
        print('--------------|---------------')
        print('     ', tn, '    |       ', fp, '      ')
        print('--------------|---------------')
        print('False negative | True positive')
        print('--------------|---------------')
        print('     ', fn, '    |       ', tp, '      ')
        print('--------------|---------------')
        print(' ')
        print(' ')
    return best_estimator


def rand_forest(X_train, X_test, y_train, y_test, estimator):
    forest = RandomForestClassifier(n_estimators=estimator, class_weight='balanced')
    forest.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    score = precision_score(y_test, y_predict)
    # Fit for feature importances with test (holdout), or full dataset?
    forest.fit(X_test, y_test)
    feat_imp = forest.feature_importances_
    return feat_imp, score


def feat_imps(X_train, y_train):
    pass


if __name__ == "__main__":
    data = pd.read_csv('wfp_pumps.csv')
    df = clean(data)
    df_india, df_malawi, df_rwanda, df_uganda = country_disaggregate(df)
    categoricals = ['geo_level_1', 'water_point_type']
    one_hot_features = ['geo_level_1_India', 'water_point_type_Phe 6 Handpump']
    full_dummied = dummify(df, categoricals)
    df_eda, X_train, X_test, y_train, y_test = split(full_dummied, categoricals, one_hot_features)
    X_smote, y_smote = upsample(X_train, y_train)
    estimator = select_rand_forest(X_smote, y_smote)
    # feat_imp, score = rand_forest(X_train, X_test, y_train, y_test, estimator)
