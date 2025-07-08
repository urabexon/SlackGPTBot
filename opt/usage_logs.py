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
    def __init__(self, db_name='slackbot.db'):

    def create_table(self):
    
    def save(self, user_id, command_type):
    
    def get_num_logs(self, user_id):
    
    def close(self):
    

class Command_Type(Enum):
    '''
    ユーザーの利用ログのコマンドタイプ
    '''
    GPT = 'gpt'
    GPT_UA = 'gpt-ua'
    GPT_CA = 'gpt-ca'
    GPT_W = 'gpt-w'
    GPT_Q = 'gpt-q'
    GPT_4 = 'gpt-4'
    GPT_4O = 'gpt-4o