"""Code for training regression model."""
import pandas as pd
import statsmodels.formula.api as smf

from sklearn.decomposition import PCA


def add_scores_emotion():
    """
    Add emotion scores.

    This is not called by train_model. Must be run seperately if desired.

    Emotion scores only available for first 256 tweets collected.

    Work done by Shaida on 11/28/17
    """
    # TEMP delete score file
    df = pd.read_csv("../../data/clean/scores.csv").drop("Unnamed: 0", axis=1)
    df_scores_emotion = pd.read_csv("../../data/clean/scores_emotion.csv").drop(['score', 'text'], axis=1)
    df = df.merge(right=df_scores_emotion, how='inner', on='id_str').drop(
        ['Unnamed: 0', ], axis=1)
    
    df['avg_score'] = (df.score_keyword + df.score_textblob_bayes_sentiment + df.score_textblob_pattern_sentiment +
                       df.anger + df.negative) / 5

    # Drop unused emotion categories
    df.drop(['anticipation', 'disgust', 'fear', 'joy', 'positive', 'sadness', 'surprise', 'trust'],
        axis=1, inplace=True)

    df.sort_values(by='avg_score', ascending=False).to_csv("../../data/clean/scores_combined.csv")
    return df


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
    import pdb; pdb.set_trace()
    return df


def train_model(score_file_path="../../data/clean/scores.csv", verbose=1):
    """TBD."""
    #import pdb; pdb.set_trace()
    df_scores = pd.read_csv(score_file_path).drop("Unnamed: 0", axis=1)[['avg_score', 'id_str']]
    df_features = pd.read_csv("../../data/clean/features_clean.csv").drop("Unnamed: 0", axis=1)
    df_model = df_features.merge(right=df_scores, how='inner', left_on='Trump_tweet_id', right_on='id_str').drop(
        ['Trump_tweet_id', 'user_id', 'id_str'], axis=1)

    # Dimensionality reduction
    df_model = first_pca_component(df=df_model, features=['user_favourites_count', 'user_friends_count',
                                   'user_statuses_count'], feature_name='user_twitter_engagement')

    # Drop features not to be used for regression
    df_model = df_model.drop(['gen_prob_Other', 'age'], axis=1)

    equation = "avg_score ~ " + " + ".join(df_model.drop('avg_score', axis=1).columns)
    results = smf.ols(equation, data=df_model).fit()

    f = open("../../reports/model_summary.txt", "w")
    f.write(str(results.summary()) + '\n')
    f.close()


if __name__ == '__main__':
    print('Adding emotion scores ...')
    add_scores_emotion()

    print('Training model ...')
    train_model(score_file_path="../../data/clean/scores_combined.csv")
