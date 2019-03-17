import pandas as pd
import numpy as np
import seaborn as sns
sns.set(style="ticks", color_codes=True)
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from collections import Counter


def clean(data):
    drop_cols = ['geo_level_7', 'geo_level_6', 'geo_level_5', 'geo_level_4', 'components', 'data_collection_year', 'water_point_id', 'alert', 'risk_based_on_age', 'risk_based_on_current_condition', 'level_of_priority_to_repair_or_replace', 'recommended_activity', 'state_of_spring_protection', 'state_of_taps', 'state_of_well', 'state_of_pump', 'state_of_apron', 'out_of_service_one_day_or_less_in_past_month',
                 'presense_of_spring_protection', 'year_spring_protection_constructed_or_reconstructed', 'presense_of_tap', 'year_taps_constructed_or_reconstructed', 'presense_of_well', 'year_well_constructed_or_reconstructed', 'presense_of_pump', 'year_pump_constructed_or_reconstructed', 'presense_of_apron', 'year_apron_constructed_or_reconstructed', 'days_out_of_service_in_last_year', 'level_of_service']
    # Geo level 7 had 7,505 NaN values, geo level 6 had 2,478, and components has 5751.
    # Others dropped for incompatability with the analysis
    df = data.drop(drop_cols, axis=1)
    df.dropna(inplace=True)
    # resulting dataframe shape after remaining NaNs are dropped: (10033, 23)
    df = df.rename(columns={"remaining_lifespan_of_spring_protection": "spring_protection_past_lifespan", "remaining_lifespan_of_taps": "taps_past_lifespan",
                            "remaining_lifespan_of_well": "well_past_lifespan", "remaining_lifespan_of_pump": "pump_past_lifespan", "remaining_lifespan_of_apron": "apron_past_lifespan"})
    # Replace blank values with 0:
    blanks = ['families_with_access_to_improved_water', 'families_without_access_to_improved_water', 'spring_protection_past_lifespan',
              'taps_past_lifespan', 'well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan', 'overall_state_of_water_point']
    for i in blanks:
        df[i].replace(" ", "0", inplace=True)
    # Other replacement:
    df['spring_protection_past_lifespan'].replace("#VALUE!", "0", inplace=True)
    df['age_since_original_construction'].replace(" ", "2017", inplace=True)
    # Change stinrg numbers to numeric values:
    numeric = ['num_families_in_community', 'families_with_access_to_improved_water', 'families_without_access_to_improved_water', 'age_since_original_construction',
               'spring_protection_past_lifespan', 'taps_past_lifespan', 'well_past_lifespan', 'pump_past_lifespan', 'apron_past_lifespan', 'overall_state_of_water_point']
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
    # Make dummies for categorical columns (drop_frist=True):
    dummies = ['geo_level_1', 'geo_level_2', 'geo_level_3', 'water_point_type']
    undummied = df
    dummy = pd.get_dummies(df[dummies], drop_first=True)
    df = df.drop(dummies, axis=1)
    df = pd.concat([dummy, df], axis=1)
    # Shape after get_dummies: (10033, 81)
    return df, undummied


if __name__ == "__main__":
    data = pd.read_csv('wfp_pumps.csv')
    df, undummied = clean(data)
