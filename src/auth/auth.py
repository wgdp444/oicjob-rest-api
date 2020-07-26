"""
認証用のモジュールです。
"""
from google.oauth2 import id_token
from google.auth.transport import requests

import os
def _google_oauth(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("CLIENT_ID"))
        print(idinfo)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('しっぱいしたんだが？？？？？')
        return idinfo
    except ValueError as e:
        print(e)
        return None

def default_auth(content_type, token=None):
    """
    基本的な認証を扱います。

    Parameters
    ----------
    content_type : str
        リクエストのコンテンツタイプ。
    token : str default=None
        google認証用のトークン。
    Returns
    ----------
    idinfo : dict or None or bool
        google認証の結果。
    Raises
    ValueError:
        googleの認証に失敗した。
    """
    if content_type.lower() != 'application/json;charset=utf-8':
        return None
    if token is None:
        return None
    idinfo = _google_oauth(token)
    return idinfo
