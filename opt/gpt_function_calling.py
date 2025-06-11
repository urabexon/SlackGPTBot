from util import get_history_identifier, get_user_identifier, calculate_num_tokens, calculate_num_tokens_by_prompt, say_ts, check_availability
from typing import List, Dict
from datetime import datetime
import json
import urllib3
import os
import asyncio

class GPT_Function_Calling_CommandExecutor():
    """ChatGPT Function Calling を使ってWeb検索利用やSlack検索利用の会話をするコマンドの実行クラス"""

    FUNCTIONS = [
        {
            "name": "get_web_search_result",
            "description": "Web検索を行い、検索結果と現在時刻を取得する。これにより最新の情報を取得できる。クエリには複数の単語を指定することができるほか、ダブルクオーテーションを使ったフレーズ検索、ハイフンを利用したマイナス検索、サイト指定やタイトルに含むもの指定、URLに含むもの指定ができる。",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "検索クエリは、'シャム猫 柴犬', '\"柴犬と三毛猫、飼うならどっち？\"', '日本橋 -東京', '三毛猫 +柴犬', 'シャム猫 filetype:pdf', '柴犬 site:example.com', 'シャム猫 -site:example.com', 'intitle:柴犬', 'inurl:cats' などを組み合わせて使う。例えば、ミノタウロスの閉じ込められた迷宮がどこにあるか知りたい場合には、 'ミノタウロス 迷宮 場所' というクエリとなる。",
                        }
                    },
                "required": ["query"],
            },
        },
        {
            "name": "get_slack_search_result",
            "description": "Slack検索を行い、検索結果と現在時刻をを取得する。クエリには検索単語に加えて from:<@{ユーザーID}> と指定すると特定のユーザーのメッセージ、in:<#{チャンネルID}> と指定すると特定のチャンネルのメッセージを検索できる。つまり <@{ユーザーID}> 形式の固有のSlackユーザーの情報や、 <#{チャンネルID}> 形式の固有のSlackチャンネルの情報について情報を取得できる。has:{絵文字コード} で、特定の絵文字を持つメッセージの検索を、 before:{YYYY-MM-DD形式の日付} 日付以前、 after:{YYYY-MM-DD形式の日付} 日付以降、 on:{YYYY-MM-DD形式の日付} その日付、 during:{YYYY-MMの月} その月のメッセージを検索する条件を追加できる。",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "検索クエリは、 'シャム猫 犬', '\"柴犬と三毛猫、飼うならどっち？\"', '日本橋 -東京', 'from:<@U0VKMCTEV>', 'in:<#C0VF1QBEK>', 'before:2022-11-25', 'after:2022-11-25', 'on:2022-11-25', 'during:2022-11'などを組み合わせて使う。例えば、ユーザー <@U0VKMCTEV> の チャンネル <#C0VF1QBEK> での 2022年11月2日から2022年11月3日までのシャム猫に関することを調べるクエリは、 'from:<@U0VKMCTEV> in:<#C0VF1QBEK> after:2022-11-02 before:2022-11-03 シャム猫' というクエリとなる",
                        }
                    },
                "required": ["query"],
            },
        },
    ]

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

        for match in matches:  # パブリックのチャンネルのメッセージのみを抽出
            if match["channel"]["is_private"] == False and match["channel"]["is_mpim"] == False:
                # JSONが大きいため、トークン数節約のため情報を絞る
                filterd_matches.append({
                    "channel_id": match["channel"]["id"],
                    "channel_name": match["channel"]["name"],
                    "text":  match["text"],
                    "timestamp": datetime.fromtimestamp(float(match["ts"])).strftime("%Y/%m/%d %H:%M:%S"),
                    "user_id": match["user"]  # usernameは古いデフォルト名なため入れない
                })
            
            if len(filterd_matches) >= 20: # 利用トークン節約のため含めるメッセージ数を制限
                break

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

