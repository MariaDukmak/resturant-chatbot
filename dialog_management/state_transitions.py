import random

from dialog_management.config import rules
from dialog_management.reasoning import consequents

'''in this file the string used for the dialog manager are contained, each state has its own set of strings, if the option random_responses is enabled the system will use random strings'''

#-----------------------------------------------------------------------
#restart option not allowed
restart_option_false = ["sorry you can't restart the conversation, please set the 'restart' option to true in the config file\n", "this operation is not allowed, please enable the 'restart' option in the config file\n"]
restart_option_false_anthropomorphic = [""]
#-----------------------------------------------------------------------
#preference changes not allowed
change_preferences_option_false = ["Sorry,you can't change the preferences, you can activate this option in the config file or, if it is activated, you can restart the conversation\n", "changing preferences is not allowed at this state of the conversation, please chenge the option in the config file or, if enabled, restart the conversation\n"]
change_preferences_option_false_anthropomorphic = [""]
#-----------------------------------------------------------------------


#STATE STRINGS

#-----------------------------------------------------------------------
#1 welcome state
welcome_strings = ["Hi, Welcome to the Cambridge restaurant system, which restaurant can I help you search today?", "Hello , welcome to the Cambridge restaurant system. You can ask for restaurants by area , price range or food type. How may I help you?"]

welcome_strings_anthropomorphic = ["Hi I'm Wall-E, Welcome to the Cambridge restaurant system, which restaurant can I help you search today?"]
#-----------------------------------------------------------------------
#1a welcome state
welcome_1a_strings = ["Hi, please write your preferences so that we can help you find the perfect restaurant!", "Dear user, you can express your preferences such as location, pricerange or food type, please try again"]

welcome_1a_strings_anthropomorphic = [""]
#-----------------------------------------------------------------------

#missing information state 2a 2b 2c
missing_information_state_main_grounding = ["The system will search a restaurant", "we will search a restaurant"]

missing_information_state_main_grounding_anthropomorphic = [""]
#missing area
missing_information_state_area = [" where do you want to eat, north, south, east, west or centre?", " in which part of the city you want to eat? north, south, east, west or centre?"]

missing_information_state_area_anthropomorphic = [" "]
#missing area grounding
missing_information_state_area_grounding = [" in the {} part of the city", " in the {} area"]

missing_information_state_area_grounding_anthropomorphic = [" "]

#missing information food
missing_information_state_food = [" what kind of food do you want to eat?", " what type of food do you want to eat?"]

missing_information_state_food_anthropomorphic = [" "]
#missing information grounding
missing_information_state_food_grounding = [" that serves {} food", " that has as specialties {} food"]

missing_information_state_food_grounding_anthropomorphic = [" "]


#missing pricerange
missing_information_state_pricerange = [" would you like something in the cheap, moderate, or expensive price range?", " you can choose between these pricerange: cheap, moderate, or expensive"]

missing_information_state_pricerange_anthropomorphic = [" "]
#missing pricerange grounding
missing_information_state_pricerange_grounding = [" where the cost is {}", " where the price is {}"]

missing_information_state_pricerange_grounding_anthropomorphic = [" "]

def missing_information_state_grounding_string_builder(preferences):

    if rules["anthropomorphic_response"]:
        #grounding part anthropomorphic
        system_response = missing_information_state_main_grounding_anthropomorphic[string_random_string_selection(0, len(missing_information_state_main_grounding_anthropomorphic)-1)]
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += missing_information_state_area_grounding_anthropomorphic[string_random_string_selection(0, len(missing_information_state_area_grounding_anthropomorphic)-1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += missing_information_state_food_grounding_anthropomorphic[string_random_string_selection(0, len(missing_information_state_food_grounding_anthropomorphic)-1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += missing_information_state_pricerange_grounding_anthropomorphic[string_random_string_selection(0, len(missing_information_state_pricerange_grounding_anthropomorphic)-1)].format(preferences[2])
        #question part, asking for the missing preference/s anthropomorphic
        system_response += "."
        if preferences[0] == 'dontcare':
            system_response += missing_information_state_area_anthropomorphic[string_random_string_selection(0, len(missing_information_state_area_anthropomorphic)-1)]
        if preferences[1] == 'dontcare':
            system_response += missing_information_state_food_anthropomorphic[string_random_string_selection(0, len(missing_information_state_food_anthropomorphic)-1)]
        if preferences[2] == 'dontcare':
            system_response += missing_information_state_pricerange_anthropomorphic[string_random_string_selection(0, len(missing_information_state_pricerange_anthropomorphic)-1)]
        return system_response
    else:
        #grounding part
        system_response = missing_information_state_main_grounding[string_random_string_selection(0, len(missing_information_state_main_grounding)-1)]
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += missing_information_state_area_grounding[string_random_string_selection(0, len(missing_information_state_area_grounding)-1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += missing_information_state_food_grounding[string_random_string_selection(0, len(missing_information_state_food_grounding)-1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += missing_information_state_pricerange_grounding[string_random_string_selection(0, len(missing_information_state_pricerange_grounding)-1)].format(preferences[2])
        #question part, asking for the missing preference/s
        system_response += "."
        if preferences[0] == 'dontcare':
            system_response += missing_information_state_area[string_random_string_selection(0, len(missing_information_state_area)-1)]
        if preferences[1] == 'dontcare':
            system_response += missing_information_state_food[string_random_string_selection(0, len(missing_information_state_food)-1)]
        if preferences[2] == 'dontcare':
            system_response += missing_information_state_pricerange[string_random_string_selection(0, len(missing_information_state_pricerange)-1)]
        return system_response
#-----------------------------------------------------------------------

#recommendation found state 5
recommendation_state_found_restaurant = ["{} is a restaurant", "{} is a nice restaurant"]
recommendation_state_found_area = [" in the {} area", " located in the {}"]
recommendation_state_found_food = [" that serves {} food", ", that has as specialties {} dishes"]
recommendation_state_found_pricerange = [" at {} prices", " that is expensive"]

recommendation_state_found_restaurant_anthropomorphic = [""]
recommendation_state_found_area_anthropomorphic = [""]
recommendation_state_found_food_anthropomorphic = [""]
recommendation_state_found_pricerange_anthropomorphic = [""]

#recommendation not found state 4
recommendation_state_not_found = ["there is no restaurant", "no restaurant found"]
recommendation_state_not_found_change_preferences = [" change the (additional) preferences for others suggestions", " change your preferences and the system will search for new recommendations"]

recommendation_state_not_found_anthropomorphic = ["I'm sooooo sorry"]
recommendation_state_not_found_change_preferences_anthropomorphic = [", if you change your preferences I can do another search in a blimp!"]

def recommendation_state_string_builder(restaurant_name, preferences):

    #anthropomorphic
    if rules["anthropomorphic_response"]:
        system_response = recommendation_state_found_restaurant_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_restaurant_anthropomorphic)-1)].format(restaurant_name)
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += recommendation_state_found_area_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_area_anthropomorphic)-1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += recommendation_state_found_food_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_food_anthropomorphic)-1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += recommendation_state_found_pricerange_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_pricerange_anthropomorphic)-1)].format(preferences[2])
        return system_response
    # non_anthropomorphic
    else:
        system_response = recommendation_state_found_restaurant[string_random_string_selection(0, len(recommendation_state_found_restaurant) - 1)].format(restaurant_name)
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += recommendation_state_found_area[string_random_string_selection(0, len(recommendation_state_found_area) - 1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += recommendation_state_found_food[string_random_string_selection(0, len(recommendation_state_found_food) - 1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += recommendation_state_found_pricerange[string_random_string_selection(0, len(recommendation_state_found_pricerange) - 1)].format(preferences[2])
        return system_response

def recommendation_state_not_found_string_builder(preferences):
    # anthropomorphic
    if rules["anthropomorphic_response"]:
        system_response = recommendation_state_not_found_anthropomorphic[string_random_string_selection(0, len(recommendation_state_not_found_anthropomorphic)-1)]
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += recommendation_state_found_area_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_area_anthropomorphic)-1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += recommendation_state_found_food_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_food_anthropomorphic)-1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += recommendation_state_found_pricerange_anthropomorphic[string_random_string_selection(0, len(recommendation_state_found_pricerange_anthropomorphic)-1)].format(preferences[2])
        system_response += "." + recommendation_state_not_found_change_preferences_anthropomorphic[string_random_string_selection(0, len(recommendation_state_not_found_change_preferences_anthropomorphic)-1)]
        return system_response
    # non_anthropomorphic
    else:
        system_response = recommendation_state_not_found[
            string_random_string_selection(0, len(recommendation_state_not_found) - 1)]
        if preferences[0] != '' and preferences[0] != 'dontcare':
            system_response += recommendation_state_found_area[
                string_random_string_selection(0, len(recommendation_state_found_area) - 1)].format(preferences[0])
        if preferences[1] != '' and preferences[1] != 'dontcare':
            system_response += recommendation_state_found_food[
                string_random_string_selection(0, len(recommendation_state_found_food) - 1)].format(preferences[1])
        if preferences[2] != '' and preferences[2] != 'dontcare':
            system_response += recommendation_state_found_pricerange[
                string_random_string_selection(0, len(recommendation_state_found_pricerange) - 1)].format(
                preferences[2])
        system_response += "." + recommendation_state_not_found_change_preferences[
            string_random_string_selection(0, len(recommendation_state_not_found_change_preferences) - 1)]

#----------------------------------------------------------------------
#give info state 6

give_information_state_main = ["Sure", "Here are the information requested"]
give_information_state_address = [", the address is {}"]
give_information_state_postcode = [", the restaurant postcode is {}"]
give_information_state_phone = [", the phone number is {}"]
give_information_state_area = [", it is located in the {}"]
give_information_state_food = [", it serves {} dishes"]
give_information_state_pricerange = [", it is {}", " the price is {}"]
give_information_state_name = [", the name is {}", ", the restaurant name is {}"]

give_information_state_main_anthropomorphic = [""]
give_information_state_address_anthropomorphic = [", "]
give_information_state_postcode_anthropomorphic = [", "]
give_information_state_phone_anthropomorphic = [", "]
give_information_state_area_anthropomorphic = [", "]
give_information_state_food_anthropomorphic = [", "]
give_information_state_pricerange_anthropomorphic = [""]
give_information_state_name_anthropomorphic = [""]

def give_information_state_string_builder(information_requested):

    # anthropomorphic
    if rules["anthropomorphic_response"]:
        system_response = give_information_state_main_anthropomorphic[string_random_string_selection(0, len(give_information_state_main_anthropomorphic)-1)]
        if information_requested[0] != '' and information_requested[0] is not None:
            system_response += give_information_state_phone_anthropomorphic[string_random_string_selection(0, len(give_information_state_phone_anthropomorphic)-1)].format(information_requested[0])
        if information_requested[1] != '' and information_requested[1] is not None:
            system_response += give_information_state_address_anthropomorphic[string_random_string_selection(0, len(give_information_state_address_anthropomorphic)-1)].format(information_requested[1])
        if information_requested[2] != '' and information_requested[2] is not None:
            system_response += give_information_state_postcode_anthropomorphic[string_random_string_selection(0, len(give_information_state_postcode_anthropomorphic)-1)].format(information_requested[2])
        if information_requested[3] != '' and information_requested[3] is not None:
            system_response += give_information_state_area_anthropomorphic[string_random_string_selection(0, len(give_information_state_area_anthropomorphic)-1)].format(information_requested[3])
        if information_requested[4] != '' and information_requested[4] is not None:
            system_response += give_information_state_food_anthropomorphic[string_random_string_selection(0, len(give_information_state_food_anthropomorphic)-1)].format(information_requested[4])
        if information_requested[5] != '' and information_requested[5] is not None:
            system_response += give_information_state_pricerange_anthropomorphic[string_random_string_selection(0, len(give_information_state_pricerange_anthropomorphic)-1)].format(information_requested[5])
        if information_requested[6] != '' and information_requested[6] is not None:
            system_response += give_information_state_name_anthropomorphic[string_random_string_selection(0, len(give_information_state_name_anthropomorphic) - 1)].format(information_requested[6])
        return system_response
    else:
        system_response = give_information_state_main[string_random_string_selection(0, len(give_information_state_main) - 1)]
        if information_requested[0] != '' and information_requested[0] is not None:
            system_response += give_information_state_phone[string_random_string_selection(0, len(give_information_state_phone) - 1)].format(information_requested[0])
        if information_requested[1] != '' and information_requested[1] is not None:
            system_response += give_information_state_address[string_random_string_selection(0, len(give_information_state_address) - 1)].format(information_requested[1])
        if information_requested[2] != '' and information_requested[2] is not None:
            system_response += give_information_state_postcode[string_random_string_selection(0, len(give_information_state_postcode) - 1)].format(information_requested[2])
        if information_requested[3] != '' and information_requested[3] is not None:
            system_response += give_information_state_area[string_random_string_selection(0, len(give_information_state_area) - 1)].format(information_requested[3])
        if information_requested[4] != '' and information_requested[4] is not None:
            system_response += give_information_state_food[string_random_string_selection(0, len(give_information_state_food) - 1)].format(information_requested[4])
        if information_requested[5] != '' and information_requested[5] is not None:
            system_response += give_information_state_pricerange[string_random_string_selection(0, len(give_information_state_pricerange) - 1)].format(information_requested[5])
        if information_requested[6] != '' and information_requested[6] is not None:
            system_response += give_information_state_name[string_random_string_selection(0, len(give_information_state_name) - 1)].format(information_requested[6])
        return system_response
#-----------------------------------------------------------------------

#end state 7
end_state = ["Thank you for choosing our system! good bye!", "Thank you, goodbye!"]

end_state_anthropomorphic = [""]
#-----------------------------------------------------------------------

def search_for_consequent(input):
    for consequent in consequents:
        if consequent in input:
            return consequent
    return None


def get_consequent_output(consequent, result, explanations):
    if explanations != None:
        if consequent in explanations:
            explanation = "because " + explanations.get(consequent)
        else:
            explanation = " "

        if result == True:
            system_output = f"the result is {consequent} {explanation}"
        else:
            system_output = f"the result is not {consequent} {explanation}"
    else:
        system_output = f"the result is not {consequent}"
    return system_output

def string_allcaps_function(string):

    if rules["all_caps"]:
        return str(string).upper()
    else:
        return str(string)

def string_random_string_selection(start_int, end_int):

    if rules["random_responses"]:
        return random.randint(start_int, end_int)
    elif rules["anthropomorphic_response"]:
        return random.randint(start_int, end_int)
    else:
        return start_int