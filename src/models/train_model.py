"""Code for training regression model."""
import pandas as pd
import statsmodels.formula.api as smf

from sklearn.decomposition import PCA


def first_pca_component(df, features, feature_name='first_pca_component'):
    """
    Replace features passed with a their top PCA component.

    Parameters:
        df :
        features :
        feature_name :

    Returns:
        pd.DataFrame : df passed with columns specified by "features" replaced with first PCA component
    """
    pca = PCA(n_components=1)
    df[feature_name] = pca.fit_transform(df[features])
    df.drop(features, axis=1, inplace=True)
    return df


def train_model(score_file_path="../../data/clean/scores.csv", verbose=1):
    """Run regression analysis and save results."""
    df_scores = pd.read_csv(score_file_path).drop("Unnamed: 0", axis=1)[['score', 'id_str']]
    df_features = pd.read_csv("../../data/clean/features_clean.csv").drop("Unnamed: 0", axis=1)
    df_model = df_features.merge(right=df_scores, how='inner', left_on='Trump_tweet_id', right_on='id_str').drop(
        ['Trump_tweet_id', 'user_id', 'id_str'], axis=1)

    # Dimensionality reduction
    df_model = first_pca_component(df=df_model, features=['user_favourites_count', 'user_friends_count',
        'user_followers_count', 'user_statuses_count'], feature_name='user_twitter_engagement')

    # Drop features not to be used for regression
    df_model = df_model.drop(['gen_prob_Other', 'age'], axis=1)

    equation = "score ~ " + " + ".join(df_model.drop('score', axis=1).columns)
    results = smf.ols(equation, data=df_model).fit()

    f = open("../../reports/model_summary.txt", "w")
    f.write(str(results.summary()) + '\n')
    f.close()


if __name__ == '__main__':
    print('Training model ...')
    train_model(score_file_path="../../data/clean/scores_combined.csv")
    #train_model(score_file_path="../../data/clean/scores_combined.csv")
