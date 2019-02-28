ucsd-soc-290-project
==============================

Final project for "Theories and Practice of Big Data for Social Scientists" (UCSD Sociology 290)  

At its core, our project aimed to understand what aspects of a political supporter on social media make them more or less negative. To give this question traction, we specifically chose to investigate what aspects of Trump re-tweeters on Twitter make them more or less negative. Additionally, we chose to operationalize a supporter’s negativeness as the amount of negative sentiment contained in the rhetoric of the Trump tweet they chose to re-broadcast (i.e., retweet).  

Project Report: https://drive.google.com/open?id=19EAamW6Agausm2IPreyd1Stu0Tp-D_e1  
Project Presentation: https://drive.google.com/open?id=13KfGAcOPTfvWngOZzbbx-l6A0K5LAtoT  


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
