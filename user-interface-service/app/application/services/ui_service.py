import logging
from infrastructure.utils.file_loader import load_json
from infrastructure.clients.http_client import HttpClient


class OrchestratorService:

    def __init__(self, httpclient: HttpClient):
        self._logger = logging.getLogger(__name__)
        self._httpclient = httpclient

    async def handle(self):
        return {'response': "" }