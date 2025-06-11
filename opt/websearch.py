from typing import List, Dict
from util import get_user_identifier, calculate_num_tokens_by_prompt, say_ts
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

MAX_TOKEN_SIZE = 128000  # トークンの最大サイズ
COMPLETION_MAX_TOKEN_SIZE = 4096  # ChatCompletionの出力の最大トークンサイズ
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE  # ChatCompletionの入力に使うトークンサイズ

def say_with_websearch(client_openai, client, message, say, using_user, question, logger):

async def get_web_search_result(query: str, logger) -> List[Dict[str, str]]: