from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
import os

class GPT_4O_CommandExecutor():
    """GPT-4oを使って添付画像を含めて会話をするコマンドの実行クラス"""

    MAX_TOKEN_SIZE = 128000  # トークンの最大サイズ
    COMPLETION_MAX_TOKEN_SIZE = 2048  # ChatCompletionの出力の最大トークンサイズ
    INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE  # ChatCompletionの入力に使うトークンサイズ

    def __init__(self, client_openai):

    def execute(self, client, message, say, context, logger):
    
    def execute_reset(self, client, message, say, context, logger):
        """GPT-4oを使って会話履歴のリセットをするコマンドの実行メソッド"""