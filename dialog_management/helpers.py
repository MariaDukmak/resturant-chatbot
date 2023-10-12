import math
import pickle
import random
from typing import List, Any, Optional
from typing import Tuple, Union

import Levenshtein
import pandas as pd
import numpy as np
from dialog_management.config import rules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# from src.baseline_models.data_prep import read_data, prep_df
# from src.machinelearning.machine_learning_helpers import vectorize_utterance, encode_label
from dialog_management.reasoning import get_additional_requirements
from dialog_management.state_transitions import recommendation_state_string_builder, end_state, welcome_strings, \
    give_information_state_string_builder, recommendation_state_not_found_string_builder, \
    missing_information_state_grounding_string_builder, welcome_1a_strings, restart_option_false, \
    change_preferences_option_false, search_for_consequent, get_consequent_output, string_allcaps_function, string_random_string_selection


def vectorize_utterance(utterance: str) -> np.array:
    """Convert string to vectors using TF vectorizer."""
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit_transform(utterance)
    return tfidf_vectorizer


def encode_label(label: str) -> np.array:
    '''Encode all classes (dialog act) to list/array.'''
    label_encoder = LabelEncoder()
    label_encoder.fit_transform(label)
    return label_encoder


def read_data(filename: str = "data/dialog_acts.dat") -> pd.DataFrame:
    '''Read data from a .dat format and return a pandas dataframe.'''
    file_content = [i.strip().split(" ", 1) for i in open(filename).readlines()]
    df = pd.DataFrame(file_content, columns=['dialog_act', 'utterance_content'])
    return df


def prep_df(df):
    '''Function that will drop duplicate utterances and also remove any capitals present in the dataset'''
    df = df.drop_duplicates(['dialog_act', 'utterance_content'])
    df.loc[:, 'utterance_content'] = df['utterance_content'].str.lower()
    return df


def get_user_input(utterance):
    user_utterance = str(input(f"\n\n {utterance}"))
    return user_utterance.lower()


def classifier_prediction(user_utterance: str) -> List[str]:
    """ A function that gets the user utterance and predicts the dialog act using saved LR model."""
    print(user_utterance)
    df = read_data()
    df = prep_df(df)
    with open('data/cleaned_data_dt.pickle', 'rb') as file:
        loaded_model = pickle.load(file)

    vectorizer = vectorize_utterance(df['utterance_content'])
    vec_user_utterance = vectorizer.transform([user_utterance])
    predictionn = loaded_model.predict(vec_user_utterance)
    label_encoder = encode_label(df['dialog_act'])
    new_dialog_state = label_encoder.inverse_transform(predictionn)
    return new_dialog_state


# def states(user_input, mode):
#
#     if mode == 'human':
#         rules['anthropomorphic_response'] = True
#     else:
#         rules['anthropomorphic_response'] = False
#
#     if state == '':
#         state = '1'
#         return random.choice(welcome_strings)
#     if state == '1':
#         return state_1_welcome(user_input, mode)
#     elif state == '1a':
#         return state_1a_welcome(user_input)
#     elif state == '2a':
#         return state_2a_ask_missing_preferences_area(user_input)
#     elif state == '2b':
#         return state_2b_ask_missing_preferences_food(user_input)
#     elif state == '2c':
#         return state_2c_ask_missing_preferences_price(user_input)
#     elif state == '3a':
#         return state_3a_ask_additional_preferences(user_input)
#     elif state == '3b':
#         return state_3b_ask_to_save_preferences(user_input)
#     elif state == '4':
#         return state_4_no_restaurants(user_input)
#     elif state == '5':
#         return state_5_recommendation(user_input)
#     elif state == '6':
#         return state_6_give_information(user_input)
#     elif state == '7':
#         return state_7_end()
#     elif state == 'end':
#         return 'end'
#
