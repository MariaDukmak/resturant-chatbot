import pandas as pd
import random

# Add the antedecents to the restaurant csv
# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('../data/restaurant_info.csv')

# Create new columns and fill it with random values
food_quality = []
crowdedness = []
length_of_stay = []

for i in range(df.shape[0]):
    food_quality.append(random.choice(["good", "bad", "mediocre"]))
    crowdedness.append(random.choice(["busy", "not_busy"]))
    length_of_stay.append(random.choice(["short", "long"]))
df['food_quality'] = food_quality
df['crowdedness'] = crowdedness
df['length_of_stay'] = length_of_stay

# Save the expanded dataframe to a new CSV file, or read from the previously saved csv
df.to_csv('restaurant_info_with_properties.csv', index=False)
df = pd.read_csv('restaurant_info_with_properties.csv')

#properties column name and value
antecedent_dict = {
    ('food', 'romanian'): 'romanian',
    ('crowdedness', 'busy'): 'busy',
    ('length_of_stay', 'long'): 'long',
    ('pricerange', 'cheap'): 'cheap',
    ('food_quality', 'good'): 'good'
}

consequents = ["touristic", "assigned_seats", "children", "romantic"]

logical_list = [
    ('and', ('good', True), ('cheap', True), (consequents[0], True), "a cheap restaurant with good food attracts tourists"),
    ('and', ('romanian', True), (consequents[0], False), "Romanian cuisine is unknown for most tourists and they prefer familiar food"),
    ('and', ('busy', True), (consequents[1], True),"in a busy restaurant the waiter decides where you sit" ),
    ('and', ('long', False), (consequents[2], True), "spending a short time is advised when taking children"),
    ('and', ('busy', True), (consequents[3], False), "a busy restaurant is not romantic"),
    ('and', ('long', True), (consequents[3], True), "spending a long time in a restaurant is romantic")
]

#reverse the order of the dictionary, so the hierarchy in the rules remains when looping trhough the list
logical_list.reverse()

#check if the logical condition "and" is true
def trial_logical_conditions(valid_properties, condition):
    operator, *operands = condition

    if operator == 'and':
        if all(valid_properties.get(prop, False) == value for prop, value in operands):
            prop, value = operands[-1]  
            valid_properties[prop] = value
            return True
        else:
            return False
    return any(valid_properties.get(prop, False) == value for prop, value in operands)

def get_additional_requirements(current_restaurant):

    # Obtain the antedecents for the current restaurant
    valid_properties = {value: False for value in antecedent_dict.values()}
    explanations = {value: False for value in antecedent_dict.values()}

    for property in antecedent_dict:
        column = str(property[0])
        value = property[1]
        for _, row in current_restaurant.iterrows():
            if row[column] == value:
                valid_properties[value] = True

    # Get the consequents
    for condition in logical_list:
        if condition[0] == 'and' and trial_logical_conditions(valid_properties, condition[:-2]):
            prop, value = condition[-2]
            valid_properties[prop] = value
            explanations[prop] = (condition[-1])
    return valid_properties, explanations






