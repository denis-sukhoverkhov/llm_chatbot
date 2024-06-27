import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage, trim_messages
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

    trimmer = trim_messages(
        max_tokens=65,
        strategy="last",
        token_counter=model,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    messages = [
        SystemMessage(content="you're a good assistant"),
        HumanMessage(content="hi! I'm bob"),
        AIMessage(content="hi!"),
        HumanMessage(content="I like vanilla ice cream"),
        AIMessage(content="nice"),
        HumanMessage(content="whats 2 + 2"),
        AIMessage(content="4"),
        HumanMessage(content="thanks"),
        AIMessage(content="no problem!"),
        HumanMessage(content="having fun?"),
        AIMessage(content="yes!"),
    ]

    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
        | prompt
        | model
    )

    response = chain.invoke(
        {
            "messages": messages + [HumanMessage(content="what's my name?")],
            "language": "English",
        }
    )
    print(response.content)

    response = chain.invoke(
        {
            "messages": messages
            + [HumanMessage(content="what math problem did i ask")],
            "language": "English",
        }
    )
    print(response.content)
