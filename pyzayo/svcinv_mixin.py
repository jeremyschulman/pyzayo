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

from pyzayo.base_client import ZayoClientBase

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

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
        key-value options as defined by the "existing-services" API endpoint
        """
        return self.paginate_records(url=ZAYO_SM_ROUTE_SERVICES, **params)
