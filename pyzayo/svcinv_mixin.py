"""
This file contains the Zayo Service Inventory related API endpoints.

References
----------
    Docs
    http://54.149.224.75/wp-content/uploads/2020/02/Service-Inventory-Wiki.pdf
"""

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import List, Dict

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from first import first

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from pyzayo.base_client import ZayoClientBase
from pyzayo.consts import ZAYO_SM_ROUTE_SERVICES

# -----------------------------------------------------------------------------
# Module Exports
# -----------------------------------------------------------------------------

__all__ = ["ZayoServiceInventoryMixin"]


class ZayoServiceInventoryMixin(ZayoClientBase):
    """ Supports the Service-Inventory API endpoints """

    def get_services(self, **params) -> List[Dict]:
        """
        Retrieve the service-inventory records given the `params` criterial
        or all.

        Other Parameters
        ----------------
        key-value options as defined by the "existing-services" API endpoint.

        The `filter` parameter, for example, supports the following
        API record fields:
           * status
           * productGroup
           * productCatagory
           * product
           * term
        """
        return self.paginate_records(url=ZAYO_SM_ROUTE_SERVICES, **params)

    def get_service_by_circuit_id(self, by_circuit_id: str, **params):
        """
        Locate the service associated with the given ciruid ID.

        Parameters
        ----------
        by_circuit_id: str
            The circuit ID string value

        Other Parameters
        ----------------
        Same as get_services() method, see for details.

        Returns
        -------
        The service record in dict form from API.
        """
        return first(
            rec
            for rec in self.paginate_records(url=ZAYO_SM_ROUTE_SERVICES, **params)
            if rec["components"][0]["circuitId"] == by_circuit_id
        )
