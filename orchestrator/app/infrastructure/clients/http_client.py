import httpx, os, logging

class HttpClient:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._client = httpx.AsyncClient()
        self._service_url = {
            'extractor': os.getenv("EXTRACTOR_DOMAIN"),
            'tools': os.getenv("TOOLS_DOMAIN"),
            'llm': os.getenv("LLM_DOMAIN")
        }

    async def post(self, service: str, endpoint: str, payload: dict, timeout: float = 5.0, headers = {"Content-Type": "application/json",}):
        try:
            self._logger.info(f"Executing post request for {self._service_url[service]} with payload {payload}")
            response = await self._client.post(
                self._service_url[service] + endpoint,
                json=payload,
                timeout=timeout,
                headers=headers
            )
            header = response.headers
            response.raise_for_status()
           
            return [response.json(), header]

        except httpx.RequestError as e:
            self._logger.error(f"Request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

        except httpx.HTTPStatusError as e:
            self._logger.error(f"Bad response: {str(e.response.text)}")
            return {"error": f"Bad response: {e.response.text}"}

    async def close(self):
        await self._client.aclose()