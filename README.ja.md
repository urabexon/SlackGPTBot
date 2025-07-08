# SlackGPTBot 👾

Slackを通じて会話人工知能のChatGPTを利用するためのBOTスクリプト。  
会話の履歴数はトークン数に応じて最大まで保持。ユーザーごと、チャンネルごとに異なる履歴を保持する。
環境構築にはOpenAIのAPIトークンとSlackのBoltのアプリケーショントークン3種が必要。  
ユーザーを過去の発言から分析したり、Web検索の結果やワークスペースの結果を加味して質問に答えることもできる。  
基本的には、 `gpt-4o-mini` のモデルを利用している。 `!gpt` コマンドは、内部的にFunction Callingを使っており「Web検索をして～して」または「Slack検索をして～して」と伝えることで検索結果を考慮した受け答えができる。 

## ボットの使い方 🗣

### 基本コマンド 🎯

- `!gpt [会話内容]`: AI(ChatGPT)との会話
- `!gpt-rs`: 会話の履歴をリセット
- `!gpt-4 [会話内容]`: GPT-4モデルとの会話
- `!gpt-4-rs`: GPT-4の履歴をリセット
- `!gpt-4o [会話内容 + 画像添付]`: GPT-4oとの画像付き会話（履歴には含まれません）
- `!gpt-4o-rs`: GPT-4oの履歴をリセット

### 分析コマンド 🕵️

- `!gpt-ua [@ユーザー名]`: 指定ユーザーのパブリック発言からユーザー分析
- `!gpt-ca [#チャンネル名]`: 指定チャンネルの内容からチャンネル分析

### 検索・外部連携 🔍

- `!gpt-w [質問]`: Web検索（DuckDuckGo）を踏まえた回答
- `!gpt-q [質問]`: パブリックチャンネルの検索結果を踏まえた回答

### ヘルプ 📘

- `!gpt-help`: 使い方の一覧を表示します

セッションの概念はありませんが、API側には不正行為検出のためSlack上のユーザーIDを渡しています。🗨️

## 環境構築 ⚙️
### OpenAI の API キーと Organization ID の取得

[OpenAI API Keys](https://beta.openai.com/account/api-keys) にアクセスし、アカウントを作成後、Secret Key を取得してください。 🧾

### Slack Bot のトークン準備

[Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started) を参考に、Slack App を作成して以下のトークンを取得します：

- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `SLACK_USER_TOKEN` 🔐

#### Bot Token Scopes（`SLACK_BOT_TOKEN`）

- `chat:write`
- `files:write`（今後の DALL·E 統合のため）
- `files:read`（GPT-4o のため）

#### User Token Scopes（`SLACK_USER_TOKEN`）

- `search:read`

#### イベント購読（Event Subscriptions）

- `message.channels`
- `message.groups`
- `message.im`
- `message.mpim`

#### manifestファイルの使用

[`config/manifest.yml`](config/manifest.yml) を Slack App に読み込むことで、上記スコープを一括設定可能です。📄

## `.env` ファイルの設定 🧾

`opt/.env` に以下のような環境変数を記述してください。

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

## 各項目の意味 🧪
- `NAME_SUFFIX`: Docker コンテナ名が重複しないようにするためのサフィックス
- `USE_ONLY_PUBLIC_CHANNEL`: パブリックチャンネルのみに制限する（True/False）
- `USE_GPT_4_COMMAND`: GPT-4関連コマンドを有効にするか
- `USE_GPT_4O_COMMAND`: GPT-4o関連コマンドを有効にするか
- `DAILY_USER_LIMIT`: ユーザーごとの1日の使用上限回数（空欄で無制限）

## 起動方法 🐳

Docker を使って以下のように実行します：
```bash
docker compose --env-file ./opt/.env up -d --build
```

停止：
```bash
docker compose --env-file ./opt/.env down
```

ログの確認：
```bash
docker compose logs
```

Python 3.9.6以上での動作を確認済みです。

## 利用ログ 📊

`opt/slackbot.db` にSQLite3形式でログが保存されます。
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

確認例（直近100件）：
```bash
sqlite3 slackbot.db "select * from usage_logs order by created_at desc limit 100;"
```

整形表示（対話形式）：
```bash
sqlite3 slackbot.db
sqlite> .headers on
sqlite> .mode column
sqlite> select * from usage_logs order by created_at desc limit 100;
```

日付ごとの利用回数：
```bash
SELECT date, COUNT(*) as count FROM usage_logs GROUP BY date ORDER BY date DESC;
```

日付×コマンド別の集計：
```bash
SELECT date, command_type, COUNT(*) as count FROM usage_logs GROUP BY date, command_type ORDER BY date DESC;
```

ユーザー別の利用数：
```bash
SELECT user_id, COUNT(*) as count FROM usage_logs GROUP BY user_id ORDER BY count DESC;
```

## LICENSE 📄
このプロジェクトはMIT Licenseのもとで公開されています。