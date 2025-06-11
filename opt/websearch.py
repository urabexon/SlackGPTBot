from typing import List, Dict
from util import get_user_identifier, calculate_num_tokens_by_prompt, say_ts
import datetime
import os
import re
import asyncio

from dotenv import load_dotenv
load_dotenv()

MAX_TOKEN_SIZE = 128000  # トークンの最大サイズ
COMPLETION_MAX_TOKEN_SIZE = 4096  # ChatCompletionの出力の最大トークンサイズ
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE  # ChatCompletionの入力に使うトークンサイズ

def say_with_websearch(client_openai, client, message, say, using_user, question, logger):
    """
    質問の答えのメッセージを送信する
    """

    logger.info(f"<@{using_user}>  さんの以下の質問にWeb検索の検索結果を踏まえて対応中\n```\n{question}\n```")
    say_ts(client, message, f"<@{using_user}>  さんの以下の質問にWeb検索の検索結果を踏まえて対応中\n```\n{question}\n```")

    usingTeam = message["team"]
    userIdentifier = get_user_identifier(usingTeam, using_user)

    say_ts(client, message, content)
    logger.info(f"user: {message['user']}, content: {content}")

async def get_web_search_result(query: str, logger) -> List[Dict[str, str]]:
    search_results = []
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        for r in ddgs.text(keywords=query, region='wt-wt', safesearch='on', timelimit='y', max_results=100): # 100件で取得
            logger.debug(f"search_result: {r}")
            search_results.append(r)
        if len(search_results) >= 100: # 100件で打ち切り
            break

    return search_results