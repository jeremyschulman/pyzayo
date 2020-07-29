from typing import Optional

from os import getenv
import asyncio

import httpx

from pyzayo.api import ZayoAPI
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

    def get_records(self, url, payload=None):
        page_sz = consts.MAX_TOP_COUNT

        default_payload = dict(paging=dict(
            top=page_sz,
            skip=0
        ))

        loop = asyncio.get_event_loop()

        # get the first payload of records and then determine if there are more
        res = loop.run_until_complete(self.api.post(url, json=payload or default_payload))
        res.raise_for_status()
        body = res.json()
        metadata = body['data']['metadata']
        records = body['data']['records']
        total_recs = metadata['totalRecordCount']

        return records


class ZayoMtcClient(ZayoClient):
    def __init__(self):
        super(ZayoMtcClient, self).__init__()
        self.api = ZayoAPI(base_url=consts.ZAYO_URL_SM,
                           access_token=self._auth_payload['access_token'])

    def get_cases(self, **params):
        return self.get_records(url=consts.ZAYO_SM_ROUTE_MTC_CASES)

    def get_impacts(self, by_circuit_id=None, by_case_num=None, **params):
        if by_case_num:
            req_filter = dict(caseNumber=by_case_num)
        elif by_circuit_id:
            req_filter = dict(circuitId=by_circuit_id)
        else:
            req_filter = None

        return self.get_records(
            url=consts.ZAYO_SM_ROUTE_MTC_IMPACTS,
            payload={
                'filter': req_filter,
            }
        )

    def get_notifs(self, by_case_num):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(self.api.get(
            url=consts.ZAYO_SM_ROUTE_MTC_NOTIFS_BY_CASE.format(case_num=by_case_num)
        ))

        res.raise_for_status()
        body = res.json()
        return body

    def get_notifs_details(self, by_name: str):
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(self.api.get(
            url=consts.ZAYO_SM_ROUTE_MTC_NOTIFS_BY_NAME.format(name=by_name)
        ))

        res.raise_for_status()
        body = res.json()
        return body
