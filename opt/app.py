import os
from dotenv import load_dotenv

load_dotenv()

# slack初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

