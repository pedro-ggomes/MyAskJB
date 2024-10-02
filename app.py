import streamlit as st
from query_data import query_rag

def main():
    st.title("ChatGPT Clone")
    st.write("This is a simple ChatGPT clone using Streamlit and OpenAI's GPT-3.")

    # Initialize session state for storing chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input
    user_input = st.text_input("You:", "")

    if st.button("Send"):
        if user_input:
            # Append user input to chat history
            st.session_state['chat_history'].append(f"You: {user_input}")

            # Generate response from GPT-3
            response = query_rag(user_input)
            st.session_state['chat_history'].append(f"Bot: {response}")

    # Display chat history
    for message in st.session_state['chat_history']:
        st.write(message)

if __name__ == "__main__":
    main()