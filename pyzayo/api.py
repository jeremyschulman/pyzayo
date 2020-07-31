"""
This module contains the class used to access the ZAYO API via asyncio.
"""

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from httpx import AsyncClient

# -----------------------------------------------------------------------------
# Module Exports
# -----------------------------------------------------------------------------

__all__ = ["ZayoAPI"]


# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


class ZayoAPI(AsyncClient):
    """
    Zayo API asyncio HTTPx client class.  Each Zayo API functional area client,
    mainteance for example, should define an attribute, `api` for example, that
    uses this class to access the Zayo API system.
    """

    def __init__(self, base_url, access_token, **kwargs):
        """ init the client with the acess token and set content for JSON """
        super().__init__(base_url=base_url, **kwargs)
        self.headers["Authorization"] = access_token
        self.headers["content-type"] = "application/json"
