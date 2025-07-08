# SlackGPTBot 👾
SlackGPTBot is a bot script for interacting with the conversational AI ChatGPT via Slack.  
It retains conversation history up to the maximum number of tokens. Separate histories are maintained per user and per channel.  
To run this bot, you'll need an OpenAI API key and three types of Slack Bolt app tokens.  
The bot can analyze users based on their recent public messages and answer questions with the help of web search or Slack workspace data.  
By default, the `gpt-4o-mini` model is used. The `!gpt` command utilizes Function Calling internally, allowing the bot to process requests like "search the web and then..." or "search Slack and then...". 🧠

## How to Use 🗣
### Basic Commands 🎯
- `!gpt [message]`: Talk with ChatGPT
- `!gpt-rs`: Reset conversation history
- `!gpt-4 [message]`: Talk with GPT-4
- `!gpt-4-rs`: Reset GPT-4 conversation history
- `!gpt-4o [message + image]`: Talk with GPT-4o using attached image (image is not stored in history)
- `!gpt-4o-rs`: Reset GPT-4o conversation history

### Analysis Commands 🕵️

- `!gpt-ua [@username]`: Analyze a specific user's public messages
- `!gpt-ca [#channel-name]`: Analyze a specific public channel's messages

### Search & Integration 🔍

- `!gpt-w [question]`: Answer using web search (DuckDuckGo)
- `!gpt-q [question]`: Answer using Slack channel search results

### Help 📘

- `!gpt-help`: Show this help message

There is no session management, but user IDs are passed to the API for abuse detection. 🗨️

## Environment Setup ⚙️

### Get Your OpenAI API Key and Organization ID

Visit [OpenAI API Keys](https://beta.openai.com/account/api-keys), sign up for an account, and retrieve your secret key. 🧾

### Prepare Slack Bot Tokens

Refer to the [Bolt Getting Started Guide](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started) to create a Slack App and get the following tokens:

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `SLACK_USER_TOKEN` 🔐

#### Bot Token Scopes (`SLACK_BOT_TOKEN`)

- `chat:write`
- `files:write` (for future DALL·E integration)
- `files:read` (required by GPT-4o)

#### User Token Scopes (`SLACK_USER_TOKEN`)

- `search:read`

#### Event Subscriptions

- `message.channels`
- `message.groups`
- `message.im`
- `message.mpim`

#### Use the `manifest.yml` File

You can load [`config/manifest.yml`](config/manifest.yml) into your Slack App to apply all scopes at once. 📄

## `.env` File Setup 🧾

Create a file at `opt/.env` and define the following variables:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxx
SLACK_USER_TOKEN=xoxp-xxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-1-xxxxxxxxxxxxxxxxx
NAME_SUFFIX=-main
USE_ONLY_PUBLIC_CHANNEL=False
USE_GPT_4_COMMAND=False
USE_GPT_4O_COMMAND=False
DAILY_USER_LIMIT=
```

## Explanation of Each Variable 🧪

- `NAME_SUFFIX`: Suffix to avoid Docker container name collisions
- `USE_ONLY_PUBLIC_CHANNEL`: Limit usage to public channels only (True/False)
- `USE_GPT_4_COMMAND`: Enable GPT-4 related commands
- `USE_GPT_4O_COMMAND`: Enable GPT-4o related commands
- `DAILY_USER_LIMIT`: Daily usage limit per user (leave empty for unlimited)

## How to Run 🐳

Run the following command with Docker:
```bash
docker compose --env-file ./opt/.env up -d --build
```

To stop:
```bash
docker compose --env-file ./opt/.env down
```

Check logs:
```bash
docker compose logs
```

Confirmed to work with Python 3.9.6 or later.

## Usage Logs 📊

Logs are stored in SQLite3 format at `opt/slackbot.db`.
```bash
CREATE TABLE IF NOT EXISTS usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date text,
    user_id text,
    command_type text,
    created_at text
);
CREATE INDEX IF NOT EXISTS idx_date_user ON usage_logs (date, user_id);
```

To check the most recent 100 logs:
```bash
sqlite3 slackbot.db "select * from usage_logs order by created_at desc limit 100;"
```

Formatted display (interactive):
```bash
sqlite3 slackbot.db
sqlite> .headers on
sqlite> .mode column
sqlite> select * from usage_logs order by created_at desc limit 100;
```

Usage count by date:
```bash
SELECT date, COUNT(*) as count FROM usage_logs GROUP BY date ORDER BY date DESC;
```

Command usage per date:
```bash
SELECT date, command_type, COUNT(*) as count FROM usage_logs GROUP BY date, command_type ORDER BY date DESC;
```

Usage count per user:
```bash
SELECT user_id, COUNT(*) as count FROM usage_logs GROUP BY user_id ORDER BY count DESC;
```

## LICENSE 📄
This project is licensed under the MIT License.










