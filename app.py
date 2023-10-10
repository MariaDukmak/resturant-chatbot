import streamlit as st
from streamlit_chat import message
import time


def generate_response(user_unput, mode):
    return 'Still working on it!'

def empty(placeholder):
    placeholder.empty()
    print('empty')
    time.sleep(1)

def app() -> None:
    st.set_page_config(
        page_title="Chatbot-Group8",
        page_icon="🎈",
        layout="wide", )

    st.sidebar.title("Restaurants Chatbot")
    st.sidebar.image('chatbot.jpg')

    st.sidebar.write(" After completing the experiment, please switch to page 2 and fill in the evaluation form")
    placeholder = st.empty()
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

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            # with chat_container.container():

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What is up?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
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
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            print(st.session_state)

    if add_radio:
        empty(placeholder)

    # with st.container():

app()