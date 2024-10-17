from gaimin_ai.http_client import HttpClient
from gaimin_ai.models.t2s import T2SRequest
from gaimin_ai.models.t2s import T2SResponse
import logging

class TextToSpeech:
    def __init__(self, client: HttpClient, debug: bool = False):
        self.client: HttpClient = client
        self.path = "text-2-speech"
        self.debug = debug
    
    def generate(self, text: str) -> T2SResponse:
        request_data = T2SRequest(
                text=text,
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = self.client.post(f"{self.path}/generate", request_dict)
        response = T2SResponse(**response.json())

        if (self.debug): logging.info(response)
        return response

    async def agenerate(self, text: str) -> T2SResponse:
        request_data = T2SRequest(
                text=text,
        )
        request_dict = request_data.model_dump(exclude_unset=True)

        if (self.debug): logging.info(request_dict)

        response = await self.client.apost(f"{self.path}/generate", request_dict)
        response = T2SResponse(**response.json())

        if (self.debug): logging.info(response)
        return response