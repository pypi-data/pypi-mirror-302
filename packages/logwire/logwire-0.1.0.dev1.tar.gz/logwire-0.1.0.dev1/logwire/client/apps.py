class AppsManager:
    _path: str = "/apps/"

    def __init__(self, logwire_client):
        self._lmc = logwire_client

    def list(self):
        resp = self._lmc._client.get(self._lmc.create_url(self._path))
        resp.raise_for_status()
        return resp.json()["apps"]

    def get(self, app_id):
        resp = self._lmc._client.get(self._lmc.create_url(self._path + app_id))
        resp.raise_for_status()
        return resp.json()

    def register(self, name, workspace_id):
        resp = self._lmc._client.post(
            self._lmc.create_url(self._path + "register"),
            json={"name": name, "workspace_id": workspace_id},
        )
        resp.raise_for_status()
        return resp.json()
