class ProxyApiClient:
    _username: str
    _password: str
    _base_proxy_url: str

    def __init__(self, username: str, password: str, base_url: str):
        self._username = username
        self._password = password
        self._base_proxy_url = base_url

    def get_proxy_ip(self) -> str:
        return self._base_proxy_url.format(self._username, self._password)