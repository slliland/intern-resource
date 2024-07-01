import os
import openai
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # 必填，如果没有微软的key，可以用申请给到的hash key
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")


def lang_chain_create_chat_completions():
    chat = ChatOpenAI(
        app_id="uOv9nxRzGmJtONU5",  # 必填,申请后提供
        app_secret="Rc9jy3Tdo0teTUrVYSv6rRf7EvMTvoeW",  # 必填,申请后提供
        user_email="songyj@foxmail.com",  # 必填,自己的邮箱
        tag="2400159201",  # 选填，应用或项目名称
        openai_api_key=OPENAI_API_KEY
    )
    messages = [
        HumanMessage(content="Hello")
    ]
    completion = chat(messages)
    print(completion)


df = pd.read_excel('/Users/songyujian/Downloads/likes.xlsx')

lang_chain_create_chat_completions()