from typing import List, Dict
from util import get_user_identifier, calculate_num_tokens_by_prompt, calculate_num_tokens, say_ts
import datetime
import os

load_dotenv()

MAX_TOKEN_SIZE = 
COMPLETION_MAX_TOKEN_SIZE =
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE

def say_channel_analysis(client_openai, client, message, say, using_user, target_channel, logger):
    logger.info(f"<@{using_user}> さんの依頼で {target_channel} について、直近のチャンネルでの発言より分析します。")
    say_ts(client, message, f"<@{using_user}> さんの依頼で {target_channel} について、直近のチャンネルでの発言より分析します。")

    count = 0
    prompt = "以下のSlack上のチャンネルの投稿情報から、このチャンネルがどのようなチャンネルなのか分析して教えてください。\n\n----------------\n\n"

    say_ts(client, message, chat_gpt_response.choices[0].message.content)
    logger.info(f"user: {message['user']}, content: {chat_gpt_response.choices[0].message.content}")
