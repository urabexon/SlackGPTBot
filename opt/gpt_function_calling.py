from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
import os

class GPT_Function_Calling_CommandExecutor():
    """ChatGPT Function Calling を使ってWeb検索利用やSlack検索利用の会話をするコマンドの実行クラス"""
