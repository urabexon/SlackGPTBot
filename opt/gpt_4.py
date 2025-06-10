from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict

class GPT_4_CommandExecutor():
    """GPT-4を使って会話をするコマンドの実行クラス"""

    MAX_TOKEN_SIZE = 8192  # トークンの最大サイズ
    COMPLETION_MAX_TOKEN_SIZE = 2048  # ChatCompletionの出力の最大トークンサイズ
    INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE  # ChatCompletionの入力に使うトークンサイズ

    def __init__(self, client_openai):
        self.history_dict : Dict[str, List[Dict[str, str]]] = {}
        self.client_openai = client_openai

    def execute(self, client, message, say, context, logger):
        """GPT-4を使って会話をするコマンドの実行メソッド"""
        using_team = message["team"]
        using_channel = message["channel"]
        history_idetifier = get_history_identifier(using_team, using_channel, message["user"])
        user_identifier = get_user_identifier(using_team, message["user"])

        prompt = context["matches"][0]

        # ヒストリー取得
        history_array: List[Dict[str, str]] = []
        if history_idetifier in self.history_dict.keys():
            history_array = self.history_dict[history_idetifier]
        history_array.append({"role": "user", "content": prompt})

        # トークンのサイズがINPUT_MAX_TOKEN_SIZEを超えたら古いものを削除する
    
    def execute_reset(self, client, message, say, context, logger):
        """GPT-4を使って会話履歴のリセットをするコマンドの実行メソッド"""
        using_team = message["team"]
        using_channel = message["channel"]
        historyIdetifier = get_history_identifier(using_team, using_channel, message["user"])

        # 履歴リセット
        self.history_dict[historyIdetifier] = []

        logger.info(f"GPT-4の <@{message['user']}> さんの <#{using_channel}> での会話の履歴をリセットしました。")
        say_ts(client, message, f"GPT-4の <@{message['user']}> さんの <#{using_channel}> での会話の履歴をリセットしました。")