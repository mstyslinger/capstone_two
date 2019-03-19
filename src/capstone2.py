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
from collections import Counter
%matplotlib inline


def clean():
    drop_cols = ['geo_level_7', 'geo_level_6', 'geo_level_5', 'geo_level_4', 'geo_level_3', 'geo_level_2', 'components', 'data_collection_year', 'water_point_id', 'alert', 'risk_based_on_age', 'risk_based_on_current_condition', 'level_of_priority_to_repair_or_replace', 'recommended_activity', 'state_of_spring_protection', 'state_of_taps', 'state_of_well', 'state_of_pump', 'state_of_apron', 'out_of_service_one_day_or_less_in_past_month', 'presense_of_spring_protection',
                 'year_spring_protection_constructed_or_reconstructed', 'presense_of_tap', 'year_taps_constructed_or_reconstructed', 'presense_of_well', 'year_well_constructed_or_reconstructed', 'presense_of_pump', 'year_pump_constructed_or_reconstructed', 'presense_of_apron', 'year_apron_constructed_or_reconstructed', 'days_out_of_service_in_last_year', 'level_of_service', 'level_of_service_score', 'families_with_access_to_improved_water', 'families_without_access_to_improved_water']
    # Geo level 7 had 7,505 NaN values, geo level 6 had 2,478, and components has 5751
    # Geo level 2: India only has 2 states in the dataset and Rwanda, Uganda, and Malawi each only have 1
    # Geo level 3 - 5: The dataframes are too small for meaningful prediction when disaggregated down to this level
    # Families with access to imporved water was exactly the same as num_families_in_community, and families w/out access showed no corelation
    # Others dropped for incompatability to the analysis
    df = data.drop(drop_cols, axis=1)
    df.dropna(inplace=True)
    # resulting dataframe shape after remaining NaNs are dropped: (10033, 23)
    df = df.rename(columns={"remaining_lifespan_of_spring_protection": "spring_protection_past_lifespan", "remaining_lifespan_of_taps": "taps_past_lifespan",
                            "remaining_lifespan_of_well": "well_past_lifespan", "remaining_lifespan_of_pump": "pump_past_lifespan", "remaining_lifespan_of_apron": "apron_past_lifespan"})
    # Replace blank values with 0:
    blanks = ['spring_protection_past_lifespan', 'taps_past_lifespan', 'well_past_lifespan',
              'pump_past_lifespan', 'apron_past_lifespan', 'overall_state_of_water_point']
    for i in blanks:
        df[i].replace(" ", "0", inplace=True)
    # replace water point technologies having less than 150 entries with "other"
    other_technologies = ['Pond', 'Unprotected Spring', 'Tara Direct Action Pump', 'Malda Handpump', 'Unprotected Well', 'River/Stream', 'Stream', 'Scoophole', 'Mark Iii Handpump',
                          'Solar Powered Borehole', 'River', 'Unprotected Shallow Well', 'Elephant Pump', 'Mark Iv Handpump', 'Sabmisable Pump', 'Canal', 'Artisan Well', 'Borehole', 'Climax']
    for i in other_technologies:
        df['water_point_type'].replace(i, "other", inplace=True)
    # Delete extra space after Uganda in geo_level_1 feature:
    df['geo_level_1'].replace('Uganda ', 'Uganda', inplace=True)
    # Other replacement:
    df['spring_protection_past_lifespan'].replace("#VALUE!", "0", inplace=True)
    df['age_since_original_construction'].replace(" ", "2017", inplace=True)
    # Change string numbers to numeric values:
    numeric = ['num_families_in_community', 'age_since_original_construction', 'spring_protection_past_lifespan',
               'taps_past_lifespan', 'well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan', 'overall_state_of_water_point']
    for i in numeric:
        df[i] = pd.to_numeric(df[i])
    # Transform years to ages:
    df['age_since_original_construction'] = df['age_since_original_construction'].apply(
        lambda x: 2017 - x)
    # Drop outlier values (typos):
    outlier_mask = (df['age_since_original_construction'] < 150) & (
        df['age_since_original_construction'] >= 0)
    df = df[outlier_mask]
    # Transform component lifespans to categorical values (1= older than lifespan, 0= within lifespan or non-existent):
    lifespans = ['spring_protection_past_lifespan', 'taps_past_lifespan',
                 'well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan']
    lifespan_mask = df[lifespans] < 0
    df[lifespans] = (lifespan_mask*1).astype(int)
    # Country disaggregated dataframes
    india_mask = df['geo_level_1'] == "India"
    df_india = df[india_mask]
    malawi_mask = df['geo_level_1'] == "Malawi"
    df_malawi = df[malawi_mask]
    rwanda_mask = df['geo_level_1'] == "Rwanda"
    df_rwanda = df[rwanda_mask]
    uganda_mask = df['geo_level_1'] == "Uganda"
    df_uganda = df[uganda_mask]
    # Make dummies for categorical columns (drop_frist=True):
    dummies = ['geo_level_1', 'water_point_type']
    alldummy = pd.get_dummies(df[dummies])
    dummy = pd.get_dummies(df[dummies], drop_first=True)
    df_dummied = df.drop(dummies, axis=1)
    all_dummied = pd.concat([alldummy, df_dummied], axis=1)
    df_dummied = pd.concat([dummy, df_dummied], axis=1)
    # dF shape (10031, 17)
    # df_dummied (drop_first) shape: (10031, 24)
    # all_dummied shape: (10031, 27)
    # df_india shape: (5991, 17)
    # df_malawi shape: (1730, 17)
    # df_rwanda shape: (743, 17)
    # df_uganda.shape: (1567, 17)
    return df, df_dummied, all_dummied, df_india, df_malawi, df_rwanda, df_uganda


def split(df_dummied):
    y = df_dummied.pop('water_available_from_point_on_day_of_visit')
    X = df_dummied
    X_train1, X_test_holdout, y_train1, y_test_holdout = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=21)
    X_train, X_test, y_train, y_test = train_test_split(
        X_train1, y_train1, test_size=0.20, stratify=y_train1, random_state=21)
    return X_test_holdout, y_test_holdout, X_train, X_test, y_train, y_test


def rand_forest():
    forest = RandomForestClassifier(n_estimators=50, random_state=21)
    forest.fit(X_train, y_train)
    feat_imp = forest.feature_importances_
    score = forest.score(X_test, y_test)  # accuracy
    # need to get recall, since false negative is worse than false positive
    return feat_imp, rf_score


if __name__ == "__main__":
    data = pd.read_csv('wfp_pumps.csv')
    df, df_dummied, all_dummied, df_india, df_malawi, df_rwanda, df_uganda = clean(data)
    X_test_holdout, y_test_holdout, X_train, X_test, y_train, y_test = split(df_dummied)
    feat_imp, rf_score = rand_forest(X_train, X_test, y_train, y_test)
