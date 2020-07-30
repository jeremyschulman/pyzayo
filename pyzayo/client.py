# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Optional, List, Dict
import math
from os import getenv
import asyncio
from itertools import chain

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import httpx
from tenacity import retry, wait_random_exponential, retry_if_exception

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------


from pyzayo import consts
from pyzayo.api import ZayoAPI

# -----------------------------------------------------------------------------
# Package Exports
# -----------------------------------------------------------------------------

__all__ = ["ZayoClient"]

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


class ZayoClient(object):
    """
    This is a base class for any Zayo Client.  This class provides the common
    functionality that would be used by subclassed clients such as the Zayo
    maintenance client, ZayoMtcClient.
    """

    def __init__(self, base_url: str):
        self._auth_payload: Optional[dict] = None
        self.authenticate()
        self.api = ZayoAPI(base_url=base_url, access_token=self.access_token)

    @property
    def access_token(self):
        return self._auth_payload["access_token"]

    def authenticate(self):
        """
        This method is used to authenticate to the Zayo API system using the
        client-id and client-secret values obtained from the environment.

        This method is called during instance initialization and the access
        token can be obtained via the `access_token` property.

        Notes
        -----
        According to the Zayo API documentation, a token is valid for 1hr. Plan
        accordingly.
        """
        client_id = getenv("ZAYO_CLIENT_ID")
        client_secret = getenv("ZAYO_CLIENT_SECRET")
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "openid",
        }
        res = httpx.post(url=consts.ZAYO_URL_AUTH, data=payload)
        res.raise_for_status()
        self._auth_payload = res.json()

    def get_records_count(self, url, **params) -> int:
        """
        This function will return the total number of records that match the
        request criteria defined by `params`.  If `params` is not provided, then
        the count of all records for the given URL.

        Parameters
        ----------
        url: str
            The route endpoint providing recoreds, for example the
            value defined in the `consts.ZAYO_SM_ROUTE_MTC_CASES`.

        Other Parameters
        ----------------
        The other `params` are key-values as defined by the Zayo API
        spec; and these are specific to the URL used.

        Returns
        -------
        The number of records matching the criterial (or all)
        """
        loop = asyncio.get_event_loop()

        # do not request any records to be returned, just need the record count
        # from the metadata response.

        payload = params.copy()
        payload["paging"] = {"top": 0}
        res = loop.run_until_complete(self.api.post(url, json=payload))
        res.raise_for_status()
        return res.json()["data"]["metadata"]["totalRecordCount"]

    def paginate_records(self, url, **params) -> List[Dict]:
        """
        This function will return all records for a given request criterial
        determined by `params` or all records.

        Parameters
        ----------
        url: str
            The API route endpoint

        Other Parameters
        ----------------
        key-values speciifc to the url being used, determines the request
        criteria.

        Notes
        -----
        The API is limited to return a maximum of 100 records per the "top" and
        "step" fields of the paging criteria.  In the event there are more than
        100 records, only the first 100 records will be returned.  The Caller
        could use the `get_records_count` to determine the total value before
        calling this function to create a better `params` criterial (perhaps by
        date range) to avoid > 100 records.

        Returns
        -------
        List of records, each dict schema is specific to the url.
        """
        if params:
            paging = params.setdefault("paging", {})
            page_sz = paging.setdefault("top", consts.MAX_TOP_COUNT)
        else:
            page_sz = consts.MAX_TOP_COUNT
            params = dict(paging=dict(top=page_sz, skip=0))

        loop = asyncio.get_event_loop()
        total_recs = self.get_records_count(url=url, **params)

        # TODO: limit to 100?  API seems to allow to page beyond skip=50 ...
        # max_recs = min(total_recs, consts.MAX_PAGED_RECORDS)

        max_recs = total_recs
        total_pages = math.ceil(max_recs / page_sz)

        tasks = list()
        print(f"paging total records {max_recs} pages {total_pages} of size {page_sz}")

        @retry(
            retry=retry_if_exception(httpx.ReadTimeout),
            wait=wait_random_exponential(multiplier=1, max=10),
        )
        async def get_page(payload):
            return await self.api.post(url, json=payload)

        for page in range(total_pages):
            task_params = params.copy()
            task_params["paging"] = {"top": page_sz, "skip": (page * page_sz)}
            tasks.append(get_page(task_params))

        http_res_list = loop.run_until_complete(
            asyncio.gather(*tasks, return_exceptions=True)
        )
        return list(
            chain.from_iterable(
                resp.json()["data"]["records"]
                for resp in http_res_list
                if resp.is_error is False
            )
        )
