from typing import List, Dict
from util import get_user_identifier, calculate_num_tokens_by_prompt, say_ts
import datetime
import os
import re

from dotenv import load_dotenv
load_dotenv()

MAX_TOKEN_SIZE = 128000
COMPLETION_MAX_TOKEN_SIZE = 4096
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE

def say_question(client_openai, client, message, say, using_user, target_channel, logger):
    """
    質問の答えのメッセージを送信する
    """

    logger.info(f"<@{using_user}>  さんの以下の質問にパブリックチャンネルの検索結果を踏まえて対応中\n```\n{question}\n```")
    say_ts(client, message, f"<@{using_user}>  さんの以下の質問にパブリックチャンネルの検索結果を踏まえて対応中\n```\n{question}\n```")

    # ChatCompletionから適切なクエリを聞く
    query_ask_prompt = f"「{question}」という質問をSlackの検索で調べるときに適切な検索クエリを教えてください。検索クエリとは単一の検索のための単語、または、複数の検索のための単語を半角スペースで繋げた文字列です。検索クエリを##########検索クエリ##########の形式で教えてください。"
    query_gpt_response = client_openai.chat.completions.create()

    logger.debug(chat_gpt_response)

    say_ts(client, message, chat_gpt_response.choices[0].message.content)