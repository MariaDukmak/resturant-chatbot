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
    change_preferences_option_false, search_for_consequent, get_consequent_output, string_allcaps_function,\
    string_random_string_selection, welcome_strings_anthropomorphic, welcome_1a_strings_anthropomorphic



def get_user_input(utterance):
    user_utterance = str(input(f"\n\n {utterance}"))
    return user_utterance.lower()


def classifier_prediction(user_utterance: str) -> List[str]:
    """ A function that gets the user utterance and predicts the dialog act using saved LR model."""
    print(user_utterance)
    df = read_data()
    df = prep_df(df)
    with open('data/new_data_lr.pickle', 'rb') as file:
        loaded_model = pickle.load(file)

    vectorizer = vectorize_utterance(df['utterance_content'])
    vec_user_utterance = vectorizer.transform([user_utterance])
    prediction = loaded_model.predict(vec_user_utterance)
    label_encoder = encode_label(df['dialog_act'])
    new_dialog_state = label_encoder.inverse_transform(prediction)
    return new_dialog_state


class DataStates:
    def __init__(self):
        self.string = ''
        self.state = ''
        self.preferences = ['','','']
        self.null_counter = 0
        self.recommendations = ''
        self.recommendation = ''
        self.recommendation_nr = 0
        self.drop_indexes = []


class StateManager:
    def __init__(self):
        self.ds = DataStates()

    def states(self, user_input, mode):
        if mode == 'human':
            rules['anthropomorphic_response'] = True
        else:
            rules['anthropomorphic_response'] = False
        print(self.ds.state)
        match self.ds.state:
            case '':
                self.ds.state = '1'
                if rules['anthropomorphic_response']:
                    return random.choice(welcome_strings_anthropomorphic)
                else:
                    return random.choice(welcome_strings)
            case '1':
                s,self.ds = state_1_welcome(user_input, self.ds)
                return s
            case '1a':
                s,self.ds = state_1a_welcome(user_input, self.ds)
                return s
            case '2a':
                s,self.ds = state_2a_ask_missing_preferences_area(user_input, self.ds)
                return s
            case '2b':
                s,self.ds = state_2b_ask_missing_preferences_food(user_input, self.ds)
                return s
            case '2c':
                s,self.ds = state_2c_ask_missing_preferences_price(user_input, self.ds)
                return s
            case '3a':
                s,self.ds = state_3a_ask_additional_preferences(user_input, self.ds)
                return s
            case '3b':
                s,self.ds = state_3b_ask_to_save_preferences(user_input, self.ds)
                return s
            case '4':
                s,self.ds = state_4_no_restaurants(user_input, self.ds)
                return s
            case '5':
                s,self.ds = state_5_recommendation(user_input, self.ds)
                return s
            case '6':
                s,self.ds = state_6_give_information(user_input, self.ds)
                return s
            case 'end':
                return 'end'

def state_1_welcome(user_input, ds):
    '''Welcome state that will start the dialogue system. If one of the preferences is dont care, ask preferences
    if all the preferences are given, search in the database'''

    new_dialog_state = classifier_prediction(user_input)
    ds.preferences = extract_preferences(user_input)

    if new_dialog_state == 'inform' or (new_dialog_state == 'null' and ds.preferences.count("dontcare") < 3) or (new_dialog_state == 'reqalts' and ds.preferences.count("dontcare") < 3) or (new_dialog_state == 'request' and ds.preferences.count("dontcare") < 3):
        if ds.preferences[0] == 'dontcare' or ds.preferences[1] == 'dontcare' or ds.preferences[2] == 'dontcare':
            return state_2_ask_missing_preferences(ds)
        else:
            return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        ds.state = '1a'
        if rules['anthropomorphic_response']:
            return welcome_1a_strings_anthropomorphic[
                string_random_string_selection(0, len(welcome_1a_strings_anthropomorphic) - 1)], clearDsClass(ds)
        else:
            return welcome_1a_strings[string_random_string_selection(0, len(welcome_1a_strings) - 1)], clearDsClass(ds)

def state_1a_welcome(user_input, ds):
    '''This state is reached if the user utterance is not inform'''

    new_dialog_state = classifier_prediction(user_input)
    ds.preferences = extract_preferences(user_input)

    if new_dialog_state == 'inform' or (new_dialog_state == 'null' and ds.preferences.count("dontcare") < 3) or (new_dialog_state == 'reqalts' and ds.preferences.count("dontcare") < 3):
        if ds.preferences[0] == 'dontcare' or ds.preferences[1] == 'dontcare' or ds.preferences[2] == 'dontcare':
            return state_2_ask_missing_preferences(ds)
        else:
            return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        ds.state = '1a'
        if rules['anthropomorphic_response']:
            return welcome_1a_strings_anthropomorphic[
                string_random_string_selection(0, len(welcome_1a_strings_anthropomorphic) - 1)], clearDsClass(ds)
        else:
            return welcome_1a_strings[string_random_string_selection(0, len(welcome_1a_strings) - 1)], clearDsClass(ds)

def state_2_ask_missing_preferences(ds):
    '''In this state we check for the missing preferences, by order is asked: area, food or price'''

    if ds.preferences[0] == '' or ds.preferences[0] == 'dontcare':
        ds.state = '2a'
        return string_allcaps_function(missing_information_state_grounding_string_builder(ds.preferences)), ds
    elif ds.preferences[1] == '' or ds.preferences[1] == 'dontcare':
        ds.state = '2b'
        return string_allcaps_function(missing_information_state_grounding_string_builder(ds.preferences)), ds
    elif ds.preferences[2] == '' or ds.preferences[2] == 'dontcare':
        ds.state = '2c'
        return string_allcaps_function(missing_information_state_grounding_string_builder(ds.preferences)), ds
    else:
        ds.state = '3'
        return state_3_database_search(ds)

def state_2a_ask_missing_preferences_area(user_input, ds):
    '''the preference missing in state 2a is area, however the system asks the user for the other missing prferences'''

    new_dialog_state = classifier_prediction(user_input)
    ds.preferences = update_preferences(ds.preferences, extract_preferences(user_input))
    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or( new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[string_random_string_selection(0, len(welcome_strings_anthropomorphic)-1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings)-1)], clearDsClass(ds)
        else:
            ds.state = '2a'
            return string_allcaps_function(restart_option_false[string_random_string_selection(0, len(restart_option_false)-1)]), ds
    elif new_dialog_state == "inform" or (new_dialog_state == 'null' and 'idontcare' in user_input):
        if ds.preferences.count("dontcare") == 3:
            ds.state = '2a'
            return state_2_ask_missing_preferences(ds)
        else:
            return state_3_database_search(ds)
    elif new_dialog_state == "null":
        if ds.null_counter < rules["max_null_input_preferences"]:
            ds.null_counter += 1
            ds.state = '2a'
            return state_2_ask_missing_preferences(ds)
        else:
            if ds.preferences.count("dontcare") == 3:
                ds.null_counter = 0
                ds.state = '2a'
                return state_2_ask_missing_preferences(ds)
            else:
                return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        ds.state = '2a'
        return state_2_ask_missing_preferences(ds)

def state_2b_ask_missing_preferences_food(user_input, ds):
    '''the preference missing in state 2b is food type, however the system asks the user for the other missing prferences'''

    new_dialog_state = classifier_prediction(user_input)
    ds.preferences = update_preferences(ds.preferences, extract_preferences(user_input))
    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            ds.state = '2b'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    elif new_dialog_state == "inform" or (new_dialog_state == 'null' and 'idontcare' in user_input):
        if ds.preferences.count("dontcare") == 3:
            ds.state = '2b'
            return state_2_ask_missing_preferences(ds)
        else:
            return state_3_database_search(ds)
    elif new_dialog_state == "null":
        if ds.null_counter < rules["max_null_input_preferences"]:
            ds.null_counter += 1
            ds.state = '2b'
            return state_2_ask_missing_preferences(ds)
        else:
            if ds.preferences.count("dontcare") == 3:
                ds.null_counter = 0
                ds.state = '2b'
                return state_2_ask_missing_preferences(ds)
            else:
                return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        ds.state = '2b'
        return state_2_ask_missing_preferences(ds)

def state_2c_ask_missing_preferences_price(user_input, ds):
    '''the preference missing in state 2c is price, however the system asks the user for the other missing prferences'''

    new_dialog_state = classifier_prediction(user_input)
    ds.preferences = update_preferences(ds.preferences, extract_preferences(user_input))
    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            ds.state = '2c'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    elif new_dialog_state == "inform" or (new_dialog_state == 'null' and 'idontcare' in user_input):
        if ds.preferences.count("dontcare") == 3:
            ds.state = '2c'
            return state_2_ask_missing_preferences(ds)
        else:
            return state_3_database_search(ds)
    elif new_dialog_state == "null":
        if ds.null_counter < rules["max_null_input_preferences"]:
            ds.null_counter += 1
            ds.state = '2c'
            return state_2_ask_missing_preferences(ds)
        else:
            if ds.preferences.count("dontcare") == 3:
                ds.null_counter = 0
                ds.state = '2c'
                return state_2_ask_missing_preferences(ds)
            else:
                return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        ds.state = '2c'
        return state_2_ask_missing_preferences(ds)

def state_3_database_search(ds):
    '''in state 3 the system will search for restaurants with the preferences that the user gave
    if at least one recommendation is found the system will go to state 5, otherwise in state 4'''

    ds.recommendations = retrieve_restaurants(ds.preferences)
    ds.recommendation_nr = 0

    if ds.recommendations is None:
        ds.state = '4'
        return recommendation_state_not_found_string_builder(ds.preferences), ds
    else:
        ds.state = '3a'
        return string_allcaps_function("Do you have additional requirements for this recommendation? (e.g. 'romantic', 'touristic', 'assigned_seats' or 'children'?) "), ds

def state_3a_ask_additional_preferences(user_input, ds):
    '''in state 3a we ask for additional preference if a recommendation is found'''

    new_dialog_state = classifier_prediction(user_input)
    consequent = search_for_consequent(user_input)
    ds.recommendations["result"] = False
    ds.drop_indexes = []
    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            ds.state = '3a'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    if consequent != None:
        s = ''
        for index, row in ds.recommendations.iterrows():
            current_restaurant = row.to_frame().transpose()
            valid_properties, explanations = get_additional_requirements(current_restaurant)
            if consequent in valid_properties:
                result = valid_properties[consequent]
                s += string_allcaps_function("For restaurant:" + str(current_restaurant.iloc[0]["restaurantname"]) + " " + get_consequent_output(consequent, result, explanations)) + '\n'
            else:
                s += string_allcaps_function("For restaurant:" + str(current_restaurant.iloc[0]["restaurantname"]) + " " + get_consequent_output(consequent, False, explanations)) + '\n'
                ds.drop_indexes.append(index)
        else:
            print(string_allcaps_function(get_consequent_output(consequent, False, None)))
        ds.state = '3b'
        return s + "\n" + "Do you want to save this recommendations? If you say no, you will be able to change preferences. (please answer with 'yes' or 'no')", ds
    else:
        ds.state = '5'
        ds.recommendation = ds.recommendations.iloc[0]
        ds.recommendations.drop(index=ds.recommendations.index[0], axis=0, inplace=True)
        return string_allcaps_function(
            "restaurants found = " + str(len(ds.recommendations.index) + 1)) + " there are " + str(len(ds.recommendations.index)) + " other restaurants that you can view\n" + string_allcaps_function(
            recommendation_state_string_builder(ds.recommendation.get(key='restaurantname'), ds.preferences)), ds


def state_3b_ask_to_save_preferences(user_input, ds):
    # Ask the user if the reasoning is correct and ask changes if not

    if "yes" in user_input:
        # Drop the recommendations that don't fit the preferences
        ds.state = '5'
        s = ''
        for index in ds.drop_indexes:
            ds.recommendations.drop(index, axis=0, inplace=True)
        if ds.recommendations.empty:
            ds.state = '4'
            return recommendation_state_not_found_string_builder(ds.preferences), ds
        else:
            ds.recommendation = ds.recommendations.iloc[0]
            ds.recommendations.drop(index=ds.recommendations.index[0], axis=0, inplace=True)
            s = string_allcaps_function(
                "restaurants found = " + str(len(ds.recommendations.index) + 1)) + " there are " + str(len(ds.recommendations.index)) + " other restaurants that you can view\n" + string_allcaps_function(
                recommendation_state_string_builder(ds.recommendation.get(key='restaurantname'), ds.preferences))
            return s, ds
    elif "no" in user_input:
        ds.state = '4'
        return recommendation_state_not_found_string_builder(ds.preferences), ds
    else:
        ds.state = '1'
        if rules['anthropomorphic_response']:
            return welcome_strings_anthropomorphic[
                string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
        else:
            return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)

def state_4_no_restaurants(user_input, ds):
    '''in state 4 the system ask the user to change its preferences so that a new attempt can be made'''

    new_dialog_state = classifier_prediction(user_input)

    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            ds.state = '4'
            return string_allcaps_function(restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    elif new_dialog_state == 'inform':
        ds.preferences = update_preferences(ds.preferences, extract_preferences(user_input))
        ds.state = '3'
        return state_3_database_search(ds)
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        ds.state = '7'
        return state_7_end(ds)
    else:
        ds.state = '3'
        return state_3_database_search(ds)

def state_5_recommendation(user_input, ds):
    '''in state 5 the system will show to the user a list of restaurants,
    the user can ask additional information about the restaurant such as phone, address, postcode, name, area, type of food
    and price'''

    new_dialog_state = classifier_prediction(user_input)

    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            if ds.recommendations.empty:
                ds.state = '4'
                return string_allcaps_function(
                    restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
            else:
                ds.state = '5'
                return string_allcaps_function(
                    restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    elif new_dialog_state == 'inform':
        if rules["allow_change_preferences"] == True:
            ds.preferences = update_preferences(ds.preferences, extract_preferences(user_input))
            return state_3_database_search(ds)
        else:
            ds.state = '1'
            return string_allcaps_function(change_preferences_option_false[string_random_string_selection(0, len(change_preferences_option_false) - 1)]), ds
    elif new_dialog_state == 'reqmore' or new_dialog_state == 'deny' or new_dialog_state == 'reqalts':
        if ds.recommendations.empty:
            ds.state = '4'
            return recommendation_state_not_found_string_builder(ds.preferences), ds
        else:
            ds.recommendation = ds.recommendations.iloc[0]
            ds.recommendations.drop(index=ds.recommendations.index[0], axis=0, inplace=True)
            ds.state = '5'
            return string_allcaps_function(
                "restaurants found = " + str(len(ds.recommendations.index) + 1)) + " there are " + str(len(ds.recommendations.index)) + " other restaurants that you can view\n" + string_allcaps_function(
                recommendation_state_string_builder(ds.recommendation.get(key='restaurantname'), ds.preferences)), ds
    elif new_dialog_state == 'request':
        requested_info = ['', '', '', '', '', '', '']
        if 'phone' in user_input:
            requested_info[0] = ds.recommendation.get(key = 'phone')
        if 'address' in user_input:
            requested_info[1] = ds.recommendation.get(key = 'addr')
        if 'post' in user_input or 'code' in user_input:
            requested_info[2] = ds.recommendation.get(key = 'postcode')
        if 'area' in user_input:
            requested_info[3] = ds.recommendation.get(key='area')
        if 'food' in user_input:
            requested_info[4] = ds.recommendation.get(key='food')
        if 'price' in user_input:
            requested_info[5] = ds.recommendation.get(key='pricerange')
        if 'name' in user_input:
            requested_info[6] = ds.recommendation.get(key='restaurantname')
        ds.state = '6'
        return string_allcaps_function(give_information_state_string_builder(requested_info)), ds
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    else:
        if ds.recommendations.empty:
            ds.state = '4'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
        else:
            ds.state = '5'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds

def state_6_give_information(user_input, ds):
    '''in state 6 the system will show to the user all the information requested and can ask for more,
    or, if the option is enabled, the user can restart the coversation'''

    new_dialog_state = classifier_prediction(user_input)

    if new_dialog_state == 'request':
        requested_info = ['', '', '', '', '', '', '']
        if 'phone' in user_input:
            requested_info[0] = ds.recommendation.get(key='phone')
        if 'address' in user_input:
            requested_info[1] = ds.recommendation.get(key='addr')
        if 'postcode' in user_input:
            requested_info[2] = ds.recommendation.get(key='postcode')
        if 'area' in user_input:
            requested_info[3] = ds.recommendation.get(key='area')
        if 'food' in user_input:
            requested_info[4] = ds.recommendation.get(key='food')
        if 'price' in user_input:
            requested_info[5] = ds.recommendation.get(key='pricerange')
        if 'name' in user_input:
            requested_info[6] = ds.recommendation.get(key='restaurantname')
        ds.state = '6'
        return string_allcaps_function(give_information_state_string_builder(requested_info)), ds
    elif new_dialog_state == 'bye' or new_dialog_state == 'thankyou':
        return state_7_end(ds)
    if new_dialog_state == 'restart' or (new_dialog_state == 'inform' and 'restart' in user_input) or (new_dialog_state == 'null' and 'restart' in user_input):
        if rules["restart"] == True:
            ds.state = '1'
            if rules['anthropomorphic_response']:
                return welcome_strings_anthropomorphic[
                    string_random_string_selection(0, len(welcome_strings_anthropomorphic) - 1)], clearDsClass(ds)
            else:
                return welcome_strings[string_random_string_selection(0, len(welcome_strings) - 1)], clearDsClass(ds)
        else:
            ds.state = '6'
            return string_allcaps_function(
                restart_option_false[string_random_string_selection(0, len(restart_option_false) - 1)]), ds
    else:
        ds.state = '6'
        return string_allcaps_function("retry, what info can I give you?"), ds


def state_7_end(ds):
    '''in this state the system greets the user, and the program terminate'''

    if rules['anthropomorphic_response']:
        return string_allcaps_function(random.choice(welcome_strings_anthropomorphic)), clearDsClass(ds)
    else:
        return string_allcaps_function(random.choice(welcome_strings)), clearDsClass(ds)


def levenshtein_distance(token, variable_ranges, preference, preference_found: bool, minimum_distance: int, closest_preference, maximum_distance: int):
    '''calculate levenshtein distance if the token is not found in the list of preferences'''
    result = 'none'
    if token in variable_ranges:
        if closest_preference != 'none' or preference_found == False:
            preference = token
            preference_found = True
        result = "continue"
    else:
        # Calculate Levenshtein distances and find the closest match
        closest_variable = min(variable_ranges, key=lambda x: Levenshtein.distance(token, x))
        if Levenshtein.distance(token, closest_variable) <= maximum_distance and Levenshtein.distance(token, closest_variable) <= minimum_distance and preference_found == False:
            minimum_distance = Levenshtein.distance(token, closest_variable)
            preference = closest_variable
            result = "continue"
    return result, preference, preference_found, minimum_distance

def update_preferences(old_preferences, new_preferences):
    '''update the preference of the user'''
    old_preferences = list(old_preferences)
    new_preferences = list(new_preferences)
    if old_preferences[0] != new_preferences[0] and new_preferences[0] != "dontcare":
        old_preferences[0] = new_preferences[0]
    if old_preferences[1] != new_preferences[1] and new_preferences[1] != "dontcare":
        old_preferences[1] = new_preferences[1]
    if old_preferences[2] != new_preferences[2] and new_preferences[2] != "dontcare":
        old_preferences[2] = new_preferences[2]
    return tuple(old_preferences)

def extract_preferences(utterance: str, levenshtein: bool = True, food_preference: Optional[str] = None, location_preference: Optional[str] = None,
                        price_preference: Optional[str] = None) \
        -> tuple[Union[Optional[str], Any], Optional[str], Optional[str]]:
    '''extract preferences function that will use the levenshtein distance if that is neccessary'''

    # Get all the possible food, price and location types from the csv and initialize the preferences if they are not filled
    data = pd.read_csv('data/restaurant_info.csv')
    food_types = data['food'].unique()
    locations = data['area'].unique()
    price_ranges = data['pricerange'].unique()
    # Remove nan values using list comprehension for Levenshtein calculation
    locations = [location for location in locations if
                 not (isinstance(location, float) and math.isnan(location))]
    food_preference = food_preference or 'dontcare'
    location_preference = location_preference or 'dontcare'
    price_preference = price_preference or 'dontcare'

    minimum_distance_location, minimum_distance_price, minimum_distance_food = 3, 3, 3
    location_found, price_found, food_found = False, False, False
    closest_location, closest_price, closest_food = 'none', 'none', 'none'

    # Split the utterance
    tokens = utterance.split()
    if rules["levenshtein"]:
        # Loop over tokens in utterance
        for token in tokens:
            # Check for Location preference using keyword matching and Levenshtein distance
            result, location_preference, location_found, minimum_distance_location = levenshtein_distance(token, locations,
                                                                                                        location_preference,
                                                                                                          location_found,
                                                                                                          minimum_distance_location,
                                                                                                          closest_location, 2)
            if result == 'continue': continue

            # Check for Price preference using keyword matching and Levenshtein distance
            result, price_preference, price_found, minimum_distance_price = levenshtein_distance(token, price_ranges,
                                                                                                          price_preference,
                                                                                                          price_found,
                                                                                                          minimum_distance_price,
                                                                                                          closest_price, 2)
            if result == 'continue': continue

            # Check for Food preference using keyword matching and Levenshtein distance
            result, food_preference, food_found, minimum_distance_food = levenshtein_distance(token, food_types,
                                                                                                          food_preference,
                                                                                                          food_found,
                                                                                                          minimum_distance_food,
                                                                                                          closest_food, 3)
            if result == 'continue': continue
    if not rules["levenshtein"]:
        for token in tokens:
            # Check for Location, Price and Food preference using keyword matching
            if token in locations and location_preference == 'dontcare':
                location_preference = token
                continue

            if token in price_ranges and price_preference == 'dontcare':
                price_preference = token
                continue

            if token in food_types and food_preference == 'dontcare':
                food_preference = token
                continue

    return location_preference, food_preference, price_preference

def retrieve_restaurants(preferences: Tuple = ('north', 'cheap', None)) -> Union[pd.DataFrame, None]:
    """A function that look up for a restaurant from the given CSV file.
       It can handel none values aka any preference.
       :returns a pd.dataframe with the lookup values or a None in case nothing matches."""

    # fetch on preferences -> done
    # if none found return "no restaurant found" -> done (return none)
    # multiple possible restaurants? choose random & store all results
    filter = []
    area, food, pricerange = preferences
    data = pd.read_csv('data/restaurant_info_with_properties.csv')


    # Create a filter based on all preferences
    filter = (data['area'] == area) if area != "dontcare" else True
    filter &= (data['food'] == food) if food != "dontcare" else True
    filter &= (data['pricerange'] == pricerange) if pricerange != "dontcare" else True

    # Apply the filter
    results = data[filter]
    return results.head() if len(results) != 0 else None


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


def clearDsClass(ds):
    ds.string = ''
    ds.state = '1'
    ds.preferences = ['', '', '']
    ds.null_counter = 0
    ds.recommendations = ''
    ds.recommendation = ''
    ds.recommendation_nr = 0
    ds.drop_indexes = []
    return ds