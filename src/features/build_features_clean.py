"""Code to turn interim features into clean features used for modelling."""
import numpy as np
import os
import pandas as pd

from pathlib import Path
from sklearn.preprocessing import Imputer, StandardScaler


def normalize_features(df, features):
    # Continuous features
    scalar = StandardScaler()
    for feature in features:
        df[feature] = scalar.fit_transform(df[feature].values.reshape(-1, 1))
    return df


def impute_missing_values(df, features):
    imputer = Imputer()
    for feature in features:
        df[feature] = imputer.fit_transform(df[feature].values.reshape(-1, 1))
    return df


def log_transform_features(df, features):
    for feature in features:
        df[feature] = df[feature].apply(np.log10).replace(-np.inf, np.nan).values.reshape(-1, 1)
    return df


def build_clean_featues(verbose=1):
    """Build clean features."""
    other_features = ['Trump_tweet_id', 'user_id']
    binary_features = ['gender_male', 'gender_female', 'is_mobile_apple', 'is_mobile_android']
    continuous_features = ['age', 'years_user_exist']
    continuous_features_logarithmic = ['user_favourites_count', 'user_friends_count', 'user_statuses_count',
        'gen_prob_BabyBoom', 'gen_prob_GenX', 'gen_prob_GenZ', 'gen_Greatest_prob', 'gen_prob_Mill',
        'gen_prob_PostGenZ', 'gen_prob_Silent', 'gen_prob_Other']
    features = other_features + binary_features + continuous_features + continuous_features_logarithmic

    df_clean = pd.DataFrame()
    for f in os.listdir('../../data/interim'):
        if verbose > 0:
            print("\tProcessing {}".format(f))
        if Path("../../data/interim/" + f.split("_")[0] + "_retweet_clean_feats.csv").is_file():
            continue
        df = pd.read_csv('../../data/interim/' + f)

        # Process binary features
        df['gender_male'] = df.gender == 'male'
        df['gender_female'] = df.gender == 'female'
        df['is_mobile_apple'] = df.is_mobile_apple.astype(int)
        df['is_mobile_android'] = df.is_mobile_android.astype(int)

        # Create Trump tweet id column
        df['Trump_tweet_id'] = f.split('_')[0]

        df = df[features]
        df_clean = df_clean.append(df)

    df_clean = log_transform_features(df_clean, continuous_features_logarithmic)
    df_clean = impute_missing_values(df_clean, continuous_features + continuous_features_logarithmic)
    df_clean = normalize_features(df_clean, continuous_features + continuous_features_logarithmic)
    df_clean.to_csv("../../data/clean/data_clean.csv")


if __name__ == '__main__':
    print('Building clean features ...')
    build_clean_featues()
