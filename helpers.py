import time
import uuid
import pandas as pd
from dialog_management.helpers import StateManager

s = StateManager()


def get_id():
    random_id = uuid.uuid4()
    return random_id


def generate_response(user_input: str, mode: str):
    return s.states(user_input, mode)


def empty(placeholder):
    placeholder.empty()
    time.sleep(1)


def save_data(id, now, dialog, consent_checked, evaluation_data):
    data = [{'id':id, 'date': now, 'dialouge': dialog, 'consent_checked':consent_checked, 'age':evaluation_data[0], 'humanlike':evaluation_data[1],
             'trust_rating':evaluation_data[2], 'chatbot_enjoy_rating': evaluation_data[3],
             'recommendation_received': evaluation_data[4], 'received_unexpected_result':evaluation_data[5],
             'additional_info':evaluation_data[6], 'mode':evaluation_data[7]}]

    df = pd.DataFrame(data, columns=['id', 'date', 'dialouge', 'age', 'humanlike', 'trust_rating', 'chatbot_enjoy_rating',
                                    'recommendation_received', 'received_unexpected_result', 'additional_info', 'mode'])
    return df

