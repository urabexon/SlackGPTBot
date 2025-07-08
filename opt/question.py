from typing import List, Dict
from util import get_user_identifier, calculate_num_tokens_by_prompt, say_ts
import datetime
import os
import re

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MAX_TOKEN_SIZE = 128000
COMPLETION_MAX_TOKEN_SIZE = 4096
INPUT_MAX_TOKEN_SIZE = MAX_TOKEN_SIZE - COMPLETION_MAX_TOKEN_SIZE

def say_question(client_openai, client, message, say, using_user, target_channel, logger):
    """
    
    """