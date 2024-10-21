import streamlit as st
from typing import Dict

from layout import Layout
from aws_service import AwsService

Configuration = Dict[str, any]


def main():
    config: Configuration = {
        "aws_profile": "genai-d",
        "llm_models": [
            # "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",  # only this model is supported by AWS as of now
            # "anthropic.claude-3-5-sonnet-20240620-v1:0",
        ],
    }

    set_state(config)
    st.session_state.layout.init()

    show_sidebar(config)
    show_chat()


def put_chat_message(role, content):
    with st.chat_message(role):
        st.markdown(content)
    st.session_state.messages.append({"role": role, "content": content})


def set_state(config: Configuration):
    # Initialize layout
    if "layout" not in st.session_state:
        st.session_state.layout = Layout()

    # Initialize AWS services
    if "aws_service" not in st.session_state:
        st.session_state.aws_service = AwsService(config.get("aws_profile"))

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize list of S3 bucket objects
    if "s3_objects" not in st.session_state:
        st.session_state.s3_objects = []


def show_sidebar(config: Configuration):
    with st.sidebar:
        st.text_input("AWS Profile", key="aws_profile", value=config.get("aws_profile"))
        llm_id = st.selectbox("LLM Model", config.get("llm_models"))
        bucket_name = st.text_input("Bucket Name")
        get_files = st.button("Get files")

        if get_files:
            if not bucket_name:
                st.error("Please enter a bucket name.", icon=":material/error:")
            else:
                objects = st.session_state.aws_service.list_files(bucket_name)
                st.session_state.s3_objects = [obj["Key"] for obj in objects]

        if st.session_state.s3_objects:
            st.divider()

            file = st.selectbox(
                "Select file from your bucket", st.session_state.s3_objects
            )


def show_chat():
    # Display chat header
    with st.chat_message("assistant"):
        st.write(
            "I'm here to help you find answers within your file. To get started, simply select the file and ask me anything related to the content."
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


if __name__ == "__main__":
    main()
