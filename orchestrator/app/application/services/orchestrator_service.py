import logging
from infrastructure.utils.file_loader import load_json
from infrastructure.clients.http_client import HttpClient
from infrastructure.parser.response_parser import ResponseParser
from infrastructure.generator.response_generator import ResponseGenerator


class OrchestratorService:

    def __init__(self, json_path: str, httpclient: HttpClient):
        self._logger = logging.getLogger(__name__)
        self._tool_list = load_json(json_path)
        self._httpclient = httpclient
        self._response_generate = ResponseGenerator(self._tool_list)
        self._parser = ResponseParser()
        self._tools_session_id = ""
        

    async def handle(self, query: str, messages: list, file_path: str):
        
        extracted_data, tool_config = await self._extract_intent_and_payload_('/', {'query': query}, 2.0)
        self._logger.info(f"Calling tool services {extracted_data} {tool_config}")
        if file_path != "" and tool_config and tool_config.get('enabled') and extracted_data.get("confidence") >= extracted_data.get("required_confidence"):
            payload = {
                "name": extracted_data.get("intent"),
                "arguments": {
                    "image_path": file_path
                }
            }
            tool_response = await self._dispatch_to_tool_(tool_config, extracted_data, payload)
            print(tool_response)
            clean_reponse = self._parser.parse((tool_response.get("result")).get("content")[0].get("text"))
            content_list = [key + ": " + value for key, value in clean_reponse.items()]
            response = {
                "intent": extracted_data.get("intent"),
                "entities": {},
                "answer": " ".join(content_list),
                "external_tools": {},
                "confidence": extracted_data.get("confidence")
            }
        else:
            messages[-1]['content'] = extracted_data.get("clean_query")
            msgs = []
            for message in messages:
                if "file_path" in message:
                    del message["file_path"]
                msgs.append(message)
            self._logger.info(f"Calling LLM services")
            response = await self._invoke_llm_('/', {"query": extracted_data.get("clean_query"), 'messages': msgs}, 5.0)
        
        self._logger.info(f"Transforming data to final response")
        final_response = self._response_generate.generate(response)
        self._logger.info(f"Final response: {final_response}")

        return {'response': final_response }

    async def _invoke_llm_(self, endpoint, payload, timeout):
        response = await self._httpclient.post('llm', endpoint, payload, timeout)
        self._logger.info(f"LLM response: {response[0]}")
        return response[0]

    
    async def _extract_intent_and_payload_(self, endpoint, payload, timeout):
        response = await self._httpclient.post('extractor', endpoint, payload, timeout)
        self._logger.info(f"Extractor response: {response[0]}")
        extracted_data = response[0].get('response')
        if extracted_data == None:
            return {}, {}
        intent = extracted_data.get("intent")
        tool_config = self._tool_list.get(intent)
        return extracted_data, tool_config

    async def _dispatch_to_tool_(self, tool_config: dict, extracted_data: dict, payload: dict):
        tool_payload = {
            "jsonrpc": "2.0",
            "id": extracted_data.get("id"),
            "method": tool_config.get("endpoint"),
            "params": payload
        }
        endpoint = "/mcp"
        response = await self._httpclient.post("tools", endpoint, tool_payload, tool_config.get("timeout"), {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
        self._logger.info(f"Tool service response: {response}")
        return response[0]
    
    async def _close_(self):
        await self._httpclient.close()