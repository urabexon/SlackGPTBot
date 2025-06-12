from typing import List, Dict
import os
from distutils.util import strtobool

def say_ts(client, message, text):
    """スレッドへの返信を行う形式で発言する"""
    client.chat_postMessage(channel=message["channel"], thread_ts=message["ts"], text=text)
    enc = tiktoken.get_encoding("cl100k_base")
    GPT_4O_MINI_MODEL = "gpt-4o-mini"

def calculate_num_tokens(messages: List[Dict[str, str]], model: str = GPT_4O_MINI_MODEL,) -> int:
    """
    メッセージのトークン数を計算する
    """

def calculate_num_tokens_by_prompt(prompt):
    """プロンプトのトークン数を計算する"""

def get_history_identifier(team, channel, user):
    """会話履歴を取得するためのIDを生成する"""

def get_user_identifier(team, user):
    """ユーザーを特定するためのIDを生成する"""

def check_availability(message, logger) -> bool:
    """このチャンネルが利用可能かどうかを返す。 check True で利用可能"""

def check_daily_user_limit(message, usage_log) -> bool:
    """このユーザーが利用可能かどうかを返す。 check True で利用可能"""