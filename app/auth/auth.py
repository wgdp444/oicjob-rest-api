"""
認証用のモジュールです。
"""
from google.oauth2 import id_token
from google.auth.transport import requests

import os

def google_oauth(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("CLIENT_ID"))
        print(idinfo)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('しっぱいしたんだが？？？？？')
        return idinfo
    except ValueError as e:
        print(e)
        return None

def default_auth(token, content_type):
    """
    基本的な認証を扱います。

    Parameters
    ----------
    token : str
        google認証用のトークン。
    content_type : str
        リクエストのコンテンツタイプ。
    Returns
    ----------
    idinfo : dict or None
        google認証の結果。
    Raises
    ValueError:
        googleの認証に失敗した。
    """
    if content_type.lower() != 'application/json;charset=utf-8':
        return None
    idinfo = google_oauth(token)
    return idinfo
