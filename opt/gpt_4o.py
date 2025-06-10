from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
import os
import requests
import base64

class GPT_4O_CommandExecutor():
    """GPT-4oを使って添付画像を含めて会話をするコマンドの実行クラス"""

    MAX_TOKEN_SIZE = 128000  # トークンの最大サイズ
    COMPLETION_MAX_TOKEN_SIZE = 2048  # ChatCompletionの出力の最大トークンサイズ
    INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE  # ChatCompletionの入力に使うトークンサイズ

    def __init__(self, client_openai):
        self.history_dict : Dict[str, List[Dict[str, str]]] = {}
        self.client_openai = client_openai

    def execute(self, client, message, say, context, logger):
        """GPT-4oを使って会話をするコマンドの実行メソッド"""
        if "team" in message:
            using_team = message["team"]
        else:
            using_team = message["files"][0]["user_team"]
        using_channel = message["channel"]
        history_idetifier = get_history_identifier(
            using_team, using_channel, message["user"])
        user_identifier = get_user_identifier(using_team, message["user"])

        prompt = context["matches"][0]

        contents = [
            {
                "type": "text",
                "text": prompt
            }
        ]

        if "files" in message:
            for file in message["files"]:
                url = file["url_private"]
                mimetype = file["mimetype"]
                SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
                url_data = requests.get(url,
                                        allow_redirects=True,
                                        headers={
                                            'Authorization': f"Bearer {SLACK_BOT_TOKEN}"},
                                        stream=True
                                        ).content
                encoded_data = base64.b64encode(url_data)
                encoded_string = encoded_data.decode('utf-8')
                contents.append({
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:{mimetype};base64,{encoded_string}"
                    }
                })

        # ヒストリーを取得
        history_array: List[Dict[str, str]] = []
        if history_idetifier in self.history_dict.keys():
            history_array = self.history_dict[history_idetifier]
        history_array.append({"role": "user", "content": contents})

        # トークンのサイズがINPUT_MAX_TOKEN_SIZEを超えたら古いものを削除
        while calculate_num_tokens(history_array) > self.INPUT_MAX_TOKEN_SIZE:
            history_array = history_array[1:]

        # 単一の発言でMAX_TOKEN_SIZEを超えたら対応できない
        if(len(history_array) == 0):
            messege_out_of_token_size = f"発言内容のトークン数が{self.INPUT_MAX_TOKEN_SIZE}を超えて、{calculate_num_tokens_by_prompt(prompt)}であったため、対応できませんでした。"
            say_ts(client, message, messege_out_of_token_size)
            logger.info(messege_out_of_token_size)
            return

        # ChatCompletionを呼び出す
    
    def execute_reset(self, client, message, say, context, logger):
        """GPT-4oを使って会話履歴のリセットをするコマンドの実行メソッド"""
        if "team" in message:
            using_team = message["team"]
        else:
            using_team = message["files"][0]["user_team"]
        using_channel = message["channel"]
        historyIdetifier = get_history_identifier(using_team, using_channel, message["user"])

        # 履歴リセット
        self.history_dict[historyIdetifier] = []

        logger.info(f"GPT-4oの <@{message['user']}> さんの <#{using_channel}> での会話の履歴をリセットしました。")
        say_ts(client, message, f"GPT-4oの <@{message['user']}> さんの <#{using_channel}> での会話の履歴をリセットしました。")