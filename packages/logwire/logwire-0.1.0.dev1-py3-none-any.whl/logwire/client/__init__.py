import httpx

from logwire.client.workspaces import WorkspaceManager
from logwire.client.apps import AppsManager
from logwire.client.logs import LogsManager


class LogWireClient:
    def __init__(self, base_url: str, verify: bool = True, timeout: int = 10):
        self.base_url = base_url
        self.verify = verify
        self.timeout = timeout
        self._client = httpx.Client(verify=self.verify, timeout=self.timeout)

        self.workspaces = WorkspaceManager(self)
        self.apps = AppsManager(self)
        self.logs = LogsManager(self)

    def create_url(self, path: str):
        return self.base_url + path
