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

    # ChatCompletionから適切なクエリを聞く
    query_ask_prompt = f"「{question}」という質問をDuckDuckGoの検索で調べるときに適切な検索クエリを教えてください。検索クエリとは単一の検索のための単語、または、複数の検索のための単語を半角スペースで繋げた文字列です。検索クエリを##########検索クエリ##########の形式で教えてください。"
    query_gpt_response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query_ask_prompt}],
        top_p=1,
        n=1,
        max_tokens=COMPLETION_MAX_TOKEN_SIZE,
        temperature=1,  # 生成する応答の多様性
        presence_penalty=0,
        frequency_penalty=0,
        logit_bias={},
        user=userIdentifier
    )
    logger.debug(query_gpt_response)
    query_gpt_response_content = query_gpt_response.choices[0].message.content

    logger.debug(f"queryGPTResponseContent: {query_gpt_response_content}")
    matches = re.match(r'^(.|\s)*##########(.*)##########(.|\s)*$', query_gpt_response_content)
    query = ""
    if matches is None:
        query = question # 検索クエリがない場合は質問そのものを検索クエリにする
    else:
        query = matches.group(2)
    
    logger.info(f"user: {message['user']}, query: `{query}`")
    search_results = asyncio.run(get_web_search_result(query, logger))

    if search_results is None or len(search_results) == 0:
        say_ts(client, message, f"「{query}」に関する検索結果が見つかりませんでした。")
        return
    
    link_references = []
    web_results = []
    link_references = "\n\n" + "".join(link_references)

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