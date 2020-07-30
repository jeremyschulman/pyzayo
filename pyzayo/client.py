from typing import Optional

from os import getenv
import asyncio

import httpx
from pyzayo import consts


class ZayoClient(object):

    def __init__(self):
        self._auth_payload: Optional[dict] = None
        self.api = None
        self.authenticate()

    def authenticate(self):
        client_id = getenv('ZAYO_CLIENT_ID')
        client_secret = getenv('ZAYO_CLIENT_SECRET')
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'openid'
        }
        res = httpx.post(url=consts.ZAYO_URL_AUTH,
                         data=payload)

        res.raise_for_status()
        self._auth_payload = res.json()

    def get_count(self, url, **params):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.api.post(url, json=params))
        res.raise_for_status()
        return res.json()['data']['metadata']['totalRecordCount']

    def get_records(self, url, params=None):
        page_sz = consts.MAX_TOP_COUNT

        default_params = dict(paging=dict(
            top=page_sz,
            skip=0
        ))

        loop = asyncio.get_event_loop()

        # get the first params of records and then determine if there are more
        res = loop.run_until_complete(self.api.post(url, json=params or default_params))
        res.raise_for_status()
        body = res.json()
        metadata = body['data']['metadata']
        records = body['data']['records']
        total_recs = metadata['totalRecordCount']

        return records


