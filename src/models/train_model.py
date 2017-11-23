import pandas as pd

def train_model(verbose=1):
    df = pd.read_csv("../../data/clean/data_clean.csv")

    df.drop('Unnamed: 0', axis=1, inplace=True)
    df_X = df.drop(['Trump_tweet_id', 'user_id', 'age', 'gen_prob_Other'], axis=1)


if __name__ == '__main__':
    print('Training model ...')
    build_clean_featues()