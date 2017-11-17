"""Scripts to turn raw data into features for modeling."""
import numpy as np
import os
import pandas as pd
import re

from agefromname import AgeFromName, GenerationFromName
from IPython.core.display import display
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
            ages.append(2017 - age_from_name.argmax(name, 'm', 2017))
        elif genders[i] == 'female':
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


def build_interim_featues(verbose=1):
    """TBD."""
    interim_features = ['first_name', 'last_name', 'gender', 'age',
        'gen_prob_BabyBoom', 'gen_prob_GenX', 'gen_prob_GenZ', 'gen_Greatest_prob', 'gen_prob_Mill',
        'gen_prob_PostGenZ', 'gen_prob_Silent', 'gen_prob_Other',
        'user_favourites_count', 'user_followers_count', 'user_friends_count', 'user_lang', 'user_statuses_count']

    for f in os.listdir('../../data/raw'):
        if verbose > 0:
            print("\tProcessing {}".format(f))
        df = pd.read_csv('../../data/raw/' + f)
        df['first_name'] = df.user_name.apply(first_name)
        df['last_name'] = df.user_name.apply(last_name)
        df['name_is_english'] = df.first_name.apply(is_english)

        # Remove users with names containing non-ASCII characters. Proxy for english names.
        if verbose > 1:
            print("Examples where first_name has non-ASCII characters:")
            print(df.first_name[df['name_is_english'] == False])
        df = df[df['name_is_english']].copy()

        # Create gender feature
        df['gender'] = infer_gender(df.first_name)

        # Create age features
        df['age'] = infer_age(df.first_name, df.gender)
        df = pd.concat([df, infer_user_generation_probs(df.first_name, df.gender)], axis=1)

        # Create location features

        # Create time since user creation feature

        # Create features based on user_description

        # Save into interim dataset
        df = df[interim_features]
        df.to_csv('../../data/interim/' + f.split('_')[0] + '_retweet_interim_feats.csv')


if __name__ == '__main__':
    print('Building interim features ...')
    build_interim_featues()
