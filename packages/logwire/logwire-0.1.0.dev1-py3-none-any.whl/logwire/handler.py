import logging
from worker import worker

import httpx


class LogWireHandler(logging.Handler):
    def __init__(
        self,
        name: str,
        workspace_id: str,
        base_url: str,
        verify: bool = True,
        timeout: int = 10,
    ):
        logging.Handler.__init__(self)

        self.name = name
        self.workspace_id = workspace_id
        self.base_url = base_url
        self.verify = verify
        self.timeout = timeout

        with httpx.Client(verify=self.verify, timeout=self.timeout) as client:
            response = (
                client.post(
                    url=self.base_url + "/apps/register",
                    json={"name": self.name, "workspace_id": self.workspace_id},
                )
                .raise_for_status()
                .json()
            )

        self.app_id = response["app_id"]
        self.run_id = response["run_id"]

    @worker
    def emit(self, record):
        try:
            with httpx.Client(verify=self.verify, timeout=self.timeout) as client:
                response = client.post(
                    url=self.base_url + f"/logs/{self.app_id}/{self.run_id}",
                    json=record.__dict__,
                )
                response.raise_for_status()
        except Exception:
            self.handleError(record)
