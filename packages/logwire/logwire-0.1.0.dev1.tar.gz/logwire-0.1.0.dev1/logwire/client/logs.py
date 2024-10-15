class LogsManager:
    _path: str = "/logs/"

    def __init__(self, logwire_client):
        self._lmc = logwire_client

    def get(self, app_id, run_id):
        resp = self._lmc._client.get(
            self._lmc.create_url(self._path + app_id + "/" + run_id)
        )
        resp.raise_for_status()
        return resp.json()
