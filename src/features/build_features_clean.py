"""Scripts to turn raw data into features used for modelling"""
import numpy as np
import pandas as pd

from pathlib import Path


def build_interim_featues(verbose=1):
    for f in os.listdir('../../data/interim'):
        if verbose > 0:
            print("\tProcessing {}".format(f))
        if Path("../../data/interim/" + f.split("_")[0] + "_retweet_clean_feats.csv").is_file():
            continue
        df = pd.read_csv('../../data/raw/' + f)

        # Process binary features
        df['gender_male'] = df.gender == 'male'
        df['gender_female']= df.gender == 'female'
        df['is_mobile_apple'] = int(df.is_mobile_apple)
        df['is_mobile_android'] = int(df.is_mobile_apple)

        # Normalize numeric columns

        # 

        #Drop columns not to be used for modelling
        #cols_to_drop = ['first_name', 'last_name', 'gender']

if __name__ == '__main__':
    print('Building clean features ...')
    build_interim_featues()
