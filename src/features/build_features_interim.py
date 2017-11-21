"""Scripts to turn raw data into features used for data exploration."""
import numpy as np
import os
import pandas as pd
import re

from agefromname import AgeFromName, GenerationFromName
from IPython.core.display import display
from pathlib import Path
from pymongo import MongoClient
from gender_detector.gender_detector import GenderDetector


# -*- coding: utf-8 -*-
def is_english(s):
    """TBD."""
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def clean_name(name):
    """Utility function to clean names by removing non alphabetic characters."""
    return re.compile('[^a-zA-Z]').sub('', name)


def first_name(s):
    """TBD."""
    first_name = clean_name(s.split()[0])
    if first_name:
        return first_name
    # return "noname" string in cases where first name is completely non-alphabetic
    return 'noname'


def last_name(s):
    """TBD."""
    last_name = clean_name(s.split()[-1])
    if last_name:
        return last_name
    # return "noname" string in cases where first name is completely non-alphabetic
    return 'noname'


def infer_gender(first_names):
    """TDB."""
    detector = GenderDetector('us')
    return first_names.apply(detector.guess)


def infer_age(first_names, genders):
    """
    Infers age using first name and gender.
    "agefromname" package used: https://github.com/JasonKessler/agefromname
    """
    age_from_name = AgeFromName()
    ages = []
    for i, name in enumerate(first_names):
        if genders[i] == 'male':
            if len(age_from_name.get_estimated_counts(name, 'm', 2017)) == 0:
                ages.append(np.nan)
            else:
                ages.append(2017 - age_from_name.argmax(name, 'm', 2017))
        elif genders[i] == 'female':
            if len(age_from_name.get_estimated_counts(name, 'f', 2017)) == 0:
                ages.append(np.nan)
            else:
                ages.append(2017 - age_from_name.argmax(name, 'f', 2017))
        else:
            ages.append(np.nan)
    return ages


def infer_user_generation_probs(first_names, genders):
    """TBD."""
    generation_list = ['gen_prob_BabyBoom', 'gen_prob_GenX', 'gen_prob_GenZ', 'gen_Greatest_prob', 'gen_prob_Mill',
    'gen_prob_PostGenZ', 'gen_prob_Silent', 'gen_prob_Other']
    
    gen_from_name = GenerationFromName()
    generation_probs = []
    for i, name in enumerate(first_names):
        if genders[i] == 'male':
            generation_probs.append(gen_from_name.get_estimated_counts(name, 'm', 2017).values.reshape(1,-1))
        elif genders[i] == 'female':
            generation_probs.append(gen_from_name.get_estimated_counts(name, 'f', 2017).values.reshape(1,-1))
        else:
            generation_probs.append(np.ones((1,8)) * np.nan)
    return pd.DataFrame(data=np.array(generation_probs).squeeze(), columns=generation_list)


def get_years_user_exists(creation_date):
    return np.abs(creation_date.str.split(expand=True).iloc[:,-1].astype(int) - 2017)


def get_source_apple(source):
    return (source.str.lower().str.find("iphone") != -1) | (source.str.lower().str.find("ipad") != -1)


def get_source_android(source):
    return source.str.lower().str.find("android") != -1


def build_interim_featues(verbose=1):
    """TBD."""
    interim_features = ['first_name', 'last_name', 'gender', 'age',
        'gen_prob_BabyBoom', 'gen_prob_GenX', 'gen_prob_GenZ', 'gen_Greatest_prob', 'gen_prob_Mill',
        'gen_prob_PostGenZ', 'gen_prob_Silent', 'gen_prob_Other',
        'years_user_exist','is_mobile_apple', 'is_mobile_android',
        'user_favourites_count', 'user_followers_count', 'user_friends_count', 'user_lang', 'user_statuses_count']

    for f in os.listdir('../../data/raw'):
        if verbose > 0:
            print("\tProcessing {}".format(f))
        if Path("../../data/interim/" + f.split("_")[0] + "_retweet_interim_feats.csv").is_file():
            df = pd.concat([pd.read_csv("../../data/interim/" + f.split("_")[0] + "_retweet_interim_feats.csv"),
                            pd.read_csv('../../data/raw/' + f)], axis=1)
        else:
            df = pd.read_csv('../../data/raw/' + f)

        if 'first_name' not in df.columns:
            df['first_name'] = df.user_name.apply(first_name)
        if 'last_name' not in df.columns:
            df['last_name'] = df.user_name.apply(last_name)

        # Create gender feature
        if 'gender' not in df.columns:
            df['gender'] = infer_gender(df.first_name)

        # Create age features
        if 'age' not in df.columns:
            df['age'] = infer_age(df.first_name, df.gender)
            df = pd.concat([df, infer_user_generation_probs(df.first_name, df.gender)], axis=1)

        # Create location features

        # Create time since user creation feature
        if 'years_user_exist' not in df.columns:
            df['years_user_exist'] = get_years_user_exists(df.user_created_at)

        # Create features based on "source" of retweet
        if 'is_mobile_apple' not in df.columns:
            df['is_mobile_apple'] = get_source_apple(df.source)
        if 'is_mobile_android' not in df.columns:
            df['is_mobile_android'] = get_source_android(df.source)

        # Create features based on user_description

        # Save into interim dataset
        df = df[interim_features]
        df.to_csv('../../data/interim/' + f.split('_')[0] + '_retweet_interim_feats.csv')


if __name__ == '__main__':
    print('Building interim features ...')
    build_interim_featues()
