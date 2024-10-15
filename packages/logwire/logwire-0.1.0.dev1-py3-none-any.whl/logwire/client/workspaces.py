class WorkspaceManager:
    _path: str = "/workspaces/"

    def __init__(self, logwire_client):
        self._lmc = logwire_client

    def list(self):
        resp = self._lmc._client.get(self._lmc.create_url(self._path))
        resp.raise_for_status()
        return resp.json()["workspaces"]

    def get(self, workspace_id):
        resp = self._lmc._client.get(self._lmc.create_url(self._path + workspace_id))
        resp.raise_for_status()
        return resp.json()

    def register(self, name):
        resp = self._lmc._client.post(
            self._lmc.create_url(self._path + "register"), json={"name": name}
        )
        resp.raise_for_status()
        return resp.json()
