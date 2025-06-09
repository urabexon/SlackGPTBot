import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

load_dotenv()

# slack初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# メンションで "!gpt ○○" と話しかけるとGPTが返答する
@app.event("app_mention")
def handle_app_mention_events(body, say):
    text = body["event"]["text"]
    user_prompt = text.replace("<@" + body["event"]["user"] + ">", "").replace("!gpt", "").strip()

    if not user_prompt:
        say("プロンプトが空です。何か話しかけてください！")
        return
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
