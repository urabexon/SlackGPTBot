import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

load_dotenv()

# slack初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
