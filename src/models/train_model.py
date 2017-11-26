import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def train_model(verbose=1):
    df_features = pd.read_csv("../../data/clean/features_clean.csv").drop("Unnamed: 0", axis=1)
    df_scores = pd.read_csv("../../data/clean/scores.csv").drop("Unnamed: 0", axis=1)
    df_model = df_features.merge(right=df_scores, how='inner', left_on='Trump_tweet_id', right_on="id_str").drop(
        ['Trump_tweet_id', 'user_id', 'id_str', 'text'], axis=1)

    # Drop features not to be used for regression
    df_model = df_model.drop(['gen_prob_Other', 'age'], axis=1)

    equation = "score ~ " + " + ".join(df_model.drop('score', axis=1).columns)
    results = smf.ols(equation, data=df_model).fit()
    
    f = open("../../reports/model_summary.txt", "w")
    f.write(str(results.summary()) + '\n')
    f.close()


if __name__ == '__main__':
    print('Training model ...')
    train_model()
