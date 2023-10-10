import streamlit as st
import time
import uuid
from google.oauth2 import service_account
import gspread
import pandas as pd


def get_id():
    # Generate a random UUID
    random_id = uuid.uuid4()
    # Convert the UUID to a string
    random_id_str = str(random_id)
    return random_id_str


def generate_response(user_input, mode):
    return 'Still working on it!'


def empty(placeholder):
    placeholder.empty()
    print('empty')
    time.sleep(1)


def save_data(id, dialog, evaluation_data):
    print("dialog", dialog)
    data = [{'id':id, 'dialouge': dialog, 'ev':evaluation_data}]
    df = pd.DataFrame(data, columns=['id', 'dialouge', 'ev'])
    print(df.head())
    return df


def app() -> None:
    st.set_page_config(
        page_title="Chatbot-Group8",
        page_icon="🎈",
        layout="wide", )

    st.sidebar.title("Restaurants Chatbot")
    st.sidebar.image('chatbot.jpg')

    st.sidebar.write("After completing the experiment, please switch to page 2 and fill in the evaluation form")
    placeholder = st.empty()
    id = get_id()
    user_dict = []
    system_dict = []
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"
        ],
    )
    client = gspread.authorize(credentials)
    sheet_id = '1Xad8Afp0sRP98zARuHqPHdDCTLdnyTaB_KxfKOnGtpc'
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    sheet = client.open_by_url(csv_url).sheet1

    with st.sidebar:
        add_radio = st.checkbox("Ready to fill in the evaluation?", value=False)
    if not add_radio:
        st.title('Chat area')

        with st.expander("Instructions"):
            st.write('''This is a restaurants recommendations chatbot. For this experiment,
                     we kindly ask you the following instructions:
                     **Choose 3 of the following cases and test with the chatbot**''')
            st.markdown("- Case 1")
            st.markdown("- Case 2")
            st.markdown("- Case 3")

            st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:40px;
            }
            </style>
            ''', unsafe_allow_html=True)
            # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Accept user input
        if prompt := st.chat_input("What is up?"):
            # Add user message to chat history
            st.session_state.messages.append({"user": prompt})
            user_dict.append(prompt)
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("system"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = generate_response(prompt, None)
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                system_dict.append(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"system": full_response})
            print(st.session_state.messages)
    if add_radio:
        empty(placeholder)

        database_df = save_data(id, st.session_state.messages, None)
        database_df = database_df.astype(str)
        sheet.insert_rows(database_df.values.tolist(), len(sheet.get_all_records()) + 2)