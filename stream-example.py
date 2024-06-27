import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging


if __name__ == "__main__":
    if os.environ["DEBUG"] == "true":
        logging.basicConfig(level=logging.DEBUG)

    model = ChatOpenAI(model="gpt-3.5-turbo")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    config = {"configurable": {"session_id": "abc15"}}
    chain = prompt | model

    store = {}

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="messages",
    )

    for r in with_message_history.stream(
        {
            "messages": [HumanMessage(content="hi! I'm todd. tell me a joke")],
            "language": "English",
        },
        config=config,
    ):
        print(r.content, end="|")
