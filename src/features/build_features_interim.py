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
    """TBD."""
    age_from_name = AgeFromName()
    
    ages = []
    for i, name in enumerate(first_names):
        if genders[i] == 'male':
            ages.append(age_from_name.get_estimated_counts(name, 'm', 2017))
        elif genders[i] == 'female':
            ages.append(age_from_name.get_estimated_counts(name, 'f', 2017))
        else:
            ages.append(np.nan)
    return ages


def infer_user_generation_probs(first_names, genders):
    """TBD."""
    generation_from_name = GenerationFromName()
    generation_list = ['Baby Boomers', 'Generation X', 'Generation Z', 'Greatest', 'Millenials', 'Post Gen Z',
        'Silent', '_other']
    
    generation_probs = []
    for i, name in enumerate(first_names):
        if genders[i] == 'male':
            generation_probs.append(generation_from_name.get_estimated_counts(name, 'm', 2017))
        elif genders[i] == 'female':
            generation_probs.append(generation_from_name.get_estimated_counts(name, 'f', 2017))
        else:
            generation_probs.append(pd.Series(np.ones(8) * np.nan, index=generation_list))
    import pdb; pdb.set_trace()
    return pd.DataFrame(generation_probs)


def build_interim_featues(verbose=0):
    """TBD."""
    for f in os.listdir('../../data/raw'):
        df = pd.read_csv('../../data/raw/' + f)
        df['first_name'] = df.user_name.apply(first_name)
        df['last_name'] = df.user_name.apply(last_name)
        df['name_is_english'] = df.first_name.apply(is_english)

        if verbose > 0:
            print("Examples where first_name has non-ASCII characters:")
            print(df.first_name[df['name_is_english'] == False])

        df = df[df['name_is_english']].copy()

        # Create gender feature
        df['gender'] = infer_gender(df.first_name)

        # Create age features
        df['age'] = infer_age(df.first_name, df.gender)
        df = pd.concat([df, infer_user_generation_probs(df.first_name, df.gender)], axis=1)

        # Save into interim dataset
        df = df[['name_is_english', 'first_name', 'last_name', 'gender', 'age',
            'Baby Boomers', 'Generation X', 'Generation Z', 'Greatest', 'Millenials', 'Post Gen Z', 'Silent', '_other']]
        df.to_csv('../../data/interim/' + f.split('_')[0] + '_retweet_interim_feats.csv')


if __name__ == '__main__':
    print('Building interim features ...')
    build_interim_featues()
