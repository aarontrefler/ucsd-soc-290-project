"""Code to turn interim features into clean features used for modelling."""
import numpy as np
import os
import pandas as pd

from pathlib import Path
from sklearn.preprocessing import StandardScaler


def normalize_features(df, features):
    # Continuous features
        scalar = StandardScaler()
        for feature in continous_features:
            df[feature] = scalar.fit(df[feature].reshape(-1, 1)).transform(df[feature])


def impute_missing_values():


def log_transform_features(df, features):
    for feature in features:
        df[feature] = df[feature].reshape(-1, 1).apply(lambda x: x + 1).apply(np.log10)
    return df


def build_clean_featues(verbose=1):
    """Build clean features."""
    logarithmic_continous_features = ['user_favourites_count', 'user_friends_count', 'user_statuses_count']
    continous_features = ['age', 'years_user_exist', 'gen_prob_BabyBoom', 'gen_prob_GenX', 'gen_prob_GenZ',
        'gen_Greatest_prob', 'gen_prob_Mill', 'gen_prob_PostGenZ', 'gen_prob_Silent', 'gen_prob_Other']

    df_clean = pd.DataFrame()
    for f in os.listdir('../../data/interim'):
        if verbose > 0:
            print("\tProcessing {}".format(f))
        if Path("../../data/interim/" + f.split("_")[0] + "_retweet_clean_feats.csv").is_file():
            continue
        df = pd.read_csv('../../data/interim/' + f)

        # Filter examples
        df = df[df.user_lang == 'en']

        # Process binary features
        df['gender_male'] = df.gender == 'male'
        df['gender_female'] = df.gender == 'female'
        df['is_mobile_apple'] = df.is_mobile_apple.astype(int)
        df['is_mobile_android'] = df.is_mobile_android.astype(int)

        # Create Trump tweet id column
        df['Trump_tweet_id'] = f.split('_')[0]

        # Drop columns not to be used for modelling
        df = df[continous_features.extend(logarithmic_continous_features.extend(
        ['Trump_tweet_id', 'user_id', 'gender_male', 'gender_female', 'is_mobile_apple', 'is_mobile_android']))]
        df_clean.append(df)

    df = log_transform_features(df, logarithmic_continous_features)
    df = impute_missing_values(df)
    df = normalize_features(df, continous_features.extend(logarithmic_continous_features))


if __name__ == '__main__':
    print('Building clean features ...')
    build_clean_featues()
