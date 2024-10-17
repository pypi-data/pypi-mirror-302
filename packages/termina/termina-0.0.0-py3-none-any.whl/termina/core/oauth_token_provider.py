# Custom OAuth token provider for the Termina Python SDK

import datetime as dt
import typing
import jwt

from ..auth.client import AuthClient
from .client_wrapper import SyncClientWrapper


class OAuthTokenProvider:
    BUFFER_IN_MINUTES = 2

    def __init__(self, *, api_key: str, client_wrapper: SyncClientWrapper):
        self._api_key = api_key
        self._access_token: typing.Optional[str] = None
        self._expires_at: dt.datetime = dt.datetime.now()
        self._auth_client = AuthClient(client_wrapper=client_wrapper)

    def get_token(self) -> str:
        if self._access_token and self._expires_at > dt.datetime.now():
            return self._access_token
        return self._refresh()

    def _refresh(self) -> str:
        token_response = self._auth_client.get_token(api_key=self._api_key)
        self._access_token = token_response.access_token
        self._expires_at = self._get_expires_at(
            access_token=token_response.access_token,
            buffer_in_minutes=self.BUFFER_IN_MINUTES,
        )
        return self._access_token

    def _get_expires_at(self, *, access_token: str, buffer_in_minutes: int):
        exp = jwt.decode(access_token, options={"verify_signature": False})["exp"]
        return dt.datetime.fromtimestamp(exp) - dt.timedelta(minutes=buffer_in_minutes)
