from httpx import AsyncClient


class ZayoAPI(AsyncClient):
    def __init__(self, base_url, access_token, **kwargs):
        super().__init__(base_url=base_url, **kwargs)
        self.headers["Authorization"] = access_token
        self.headers["content-type"] = "application/json"