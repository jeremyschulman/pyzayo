from typing import List, Dict
import asyncio

from pyzayo.api import ZayoAPI
from pyzayo.client import ZayoClient
from pyzayo import consts


class ZayoMtcClient(ZayoClient):
    """
    This class defines the Zayo Maintenace API client instance.

    References
    ----------
    API documentation:
    http://54.149.224.75/wp-content/uploads/2020/03/Maintenance-Cases-Wiki.pdf
    """

    def __init__(self):
        super(ZayoMtcClient, self).__init__()
        self.api = ZayoAPI(
            base_url=consts.ZAYO_URL_SM, access_token=self._auth_payload["access_token"]
        )

    def get_cases(self, **params) -> List[Dict]:
        """
        Returns the maintenance cases.  If `params` are provided they are used
        as-is in the body-request per the API spec.  For example

            filter={'caseNumber': 'TNN-0003153584"}
            paging={'top': 5}

        Parameters
        ----------
        params

        Returns
        -------
        List[Dict]
        """
        return self.get_records(url=consts.ZAYO_SM_ROUTE_MTC_CASES, params=params)

    def get_impacts(self, by_circuit_id=None, by_case_num=None, **params) -> List[Dict]:
        """
        Get the maintenance impact records.  If `by_circuid_id` or `by_case_num`
        are provided, then these are the primary request criteria.  If not provided
        then all impact records are requested subject to any additional `params`.

        Parameters
        ----------
        by_circuit_id: str
            The circuit ID to match impact records

        by_case_num: str
            The case number to match impact records


        Other Parameters
        ----------------
        Used as-is per the API spec for request matching.


        Returns
        -------
        List of impact records matching the request criteria.
        """
        if by_case_num:
            req_filter = dict(caseNumber=by_case_num)
        elif by_circuit_id:
            req_filter = dict(circuitId=by_circuit_id)
        else:
            req_filter = {}

        return self.get_records(
            url=consts.ZAYO_SM_ROUTE_MTC_IMPACTS,
            params={"filter": req_filter, **params},
        )

    def get_notifications(self, by_case_num) -> List[Dict]:
        """
        Get notifications by case number.

        Parameters
        ----------
        by_case_num: str
            The case number to match

        Returns
        -------
        List of notification records.
        """
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(
            self.api.get(
                url=consts.ZAYO_SM_ROUTE_MTC_NOTIFS_BY_CASE.format(case_num=by_case_num)
            )
        )

        res.raise_for_status()
        body = res.json()
        return body["data"]

    def get_notification_details(self, by_name: str) -> Dict:
        """
        For a given ntoficication by "name" return the details dictionary.

        Parameters
        ----------
        by_name: str
            The notification name, begins with "MNN-"

        Returns
        -------
        The detail record; refer to API spec for key-value fields.
        """
        loop = asyncio.get_event_loop()

        res = loop.run_until_complete(
            self.api.get(
                url=consts.ZAYO_SM_ROUTE_MTC_NOTIFS_BY_NAME.format(name=by_name)
            )
        )

        res.raise_for_status()
        body = res.json()
        return body["data"]
