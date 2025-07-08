import sqlite3
from datetime import datetime
from enum import Enum

class Usage_Logs:
    '''
    ユーザーの利用ログを保存、取得するActiveRecordタイプの実装クラス

    基本ログの挿入と読み取りのみのため、マルチスレッドからの同時アクセスであっても
    そこまで大きな問題は起こらない想定。
    またこのクラスのインスタンスを一度でも作ったら、それ以降は同じインスタンスを使い回すことを想定している。
    よってDBのクローズは行わない。
    '''

class Command_Type(Enum):
    '''
    ユーザーの利用ログのコマンドタイプ
    '''
    CHAT = 1
    IMAGE = 2
    