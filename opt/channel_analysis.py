from typing import List, Dict
import os

load_dotenv()

MAX_TOKEN_SIZE = 
COMPLETION_MAX_TOKEN_SIZE =
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE

def say_channel_analysis(client_openai, client, message, say, using_user, target_channel, logger):
    