ucsd-soc-290-project
==============================

Final project for "Theories and Practice of Big Data for Social Scientists" (UCSD Sociology 290)

Project Organization
------------

    ├── README.md
    ├── data
    │   ├── interim                          <- Transformed features.
    │   ├── clean                            <- Features and scores used for modeling.
    │   ├── raw                              <- Raw features.
    │   └── twitterdb                        <- Original data.
    │
    ├── notebooks                            <- Jupyter notebooks.
    │
    ├── references                           <- Explanatory materials.
    │
    ├── reports                              <- Model output.
    │   └── figures
    │
    ├── src                                  <- Source code for use in this project.
    │   ├── __init__.py
    │   │
    │   ├── data
    │   │   ├── make_dataset_extract.py      <- Extract twitter data from Twitter and save as zipped MongoDB
    │       └── make_dataset_raw.py          <- Load zipped MongoDB
    │   │
    │   ├── features                         <- Scripts to turn raw data into features and scores for modeling
    │   │   ├── build_features_raw.py
    │   │   ├── build_features_interim.py
    │   │   ├── build_features_clean.py 
    │   │   └── build_scores.py
    │   │
    │   ├── models                           <- Scripts to train models
    │   │   └── train_model.py


--------