from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
from datetime import datetime
import json
import urllib3
import os
import asyncio

class GPT_Function_Calling_CommandExecutor():
    """ChatGPT Function Calling を使ってWeb検索利用やSlack検索利用の会話をするコマンドの実行クラス"""

    FUNCTIONS = []

    MAX_TOKEN_SIZE = 128000  # トークンの最大サイズ
    COMPLETION_MAX_TOKEN_SIZE = 4096  # ChatCompletionの出力の最大トークンサイズ
    # ChatCompletionの入力に使うトークンサイズ、FUNCTION分はJSON化してプロンプトとして雑に計算する(トークン計算方法不明のため)
    INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - \ 
        COMPLETION_MAX_TOKEN_SIZE - \
        calculate_num_tokens_by_prompt(json.dumps(FUNCTIONS, ensure_ascii=False))

    def __init__(self, client_openai):
        self.history_dict: Dict[str, List[Dict[str, str]]] = {}
        self.client_openai = client_openai
    
    async def get_web_search_result(self, query):
        """Web検索を実行する、Function Calling用実装 (100件固定)"""
        search_results = []
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            for r in ddgs.text(query, region='wt-wt', safesearch='on', timelimit='y', max_results=100):  # 100件で取得
                search_results.append(r)
                if len(search_results) >= 100: # 100件で打ち切りにする
                    break
        return {
            "search_results": search_results,
            "current_time": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }
    
    def get_slack_search_result(self, query, client):
        """Slack検索を実行する、Function Calling用実装 (100件固定)"""
        search_response = client.search_messages(token=os.getenv("SLACK_USER_TOKEN"), query=query, count=100, highlight=False)
        matches = search_response["messages"]["matches"]
        filterd_matches = []

        return {
            "search_results": filterd_matches,
            "current_time": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }
    
    def execute(self, client, message, say, context, logger):
        """Function Callingを使って会話をするコマンドの実行メソッド"""
        using_team = message["team"]
        using_channel = message["channel"]
        history_idetifier = get_history_identifier(using_team, using_channel, message["user"])
        user_identifier = get_user_identifier(using_team, message["user"])

        prompt = context["matches"][0]

    
    def execute_reset(self, client, message, say, context, logger):
        """ChatGPT Function Callingを使った会話履歴のリセットをするコマンドの実行メソッド"""
        using_team = message["team"]
        using_channel = message["channel"]
        historyIdetifier = get_history_identifier(using_team, using_channel, message["user"])

        