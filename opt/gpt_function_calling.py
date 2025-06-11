from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
import os

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
    
    async def get_web_search_result(self, query):
        """Web検索を実行する、Function Calling用実装 (100件固定)"""
    
    def get_slack_search_result(self, query, client):
        """Slack検索を実行する、Function Calling用実装 (100件固定)"""
    
    def execute(self, client, message, say, context, logger):
        """Function Callingを使って会話をするコマンドの実行メソッド"""
    
    def execute_reset(self, client, message, say, context, logger):
        """ChatGPT Function Callingを使った会話履歴のリセットをするコマンドの実行メソッド"""
