import streamlit as st

from layout import Layout


def main():
    if "layout" not in st.session_state:
        st.session_state.layout = Layout()

    st.session_state.layout.init()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat header
    with st.chat_message("assistant"):
        st.write(
            "I'm here to help you find answers within your file. To get started, simply select the file and ask me anything related to the content."
        )

    file = st.selectbox(
        "Select file from your bucket", ["First file", "Second file", "Third file"]
    )

    # Display chat history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display chat user input
    if prompt := st.chat_input("Ask your question..."):
        put_chat_message("user", prompt)

        # if response := model.get_llm_response(prompt, policy, language_code):
        put_chat_message("assistant", "response")


def put_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)
    st.session_state.messages.append({"role": role, "content": content})


if __name__ == "__main__":
    main()
