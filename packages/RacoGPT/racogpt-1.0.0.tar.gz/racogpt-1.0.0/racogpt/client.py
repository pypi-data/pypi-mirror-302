import requests
import json

class RacoGPTClient:
    def __init__(self, host="http://localhost:11434", model="RacoGPT"):
        self.host = host
        self.model = model

    def _build_simple_payload(self, query):
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False
        }

    def _build_function_call_payload(self, query, tools):
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert in composing functions. You are given a question and a set of possible functions. "
                        "Based on the question, you will need to make one or more function/tool calls to achieve the purpose. "
                        "If none of the functions can be used, point it out and refuse to answer. If the given question lacks the parameters "
                        "required by the function, also point it out. The output MUST strictly adhere to the following format, and NO other text "
                        "MUST be included. The example format is as follows. Please make sure the parameter type is correct. If no function call is "
                        "needed, please make the tool calls an empty list '[]'. ```<tool_call>[{\"name\": \"func_name1\", \"arguments\": {\"argument1\": "
                        "\"value1\", \"argument2\": \"value2\"}},... (more tool calls as required)]</tool_call>"
                    )
                },
                {
                    "role": "user",
                    "content": json.dumps({"query": query, "tools": tools})
                }
            ],
            "stream": False
        }

    def _extract_content(self, result):
        # Prima decodifica della risposta per ottenere la stringa JSON originale
        content_str = result["message"]["content"]

        # Carica il contenuto per ottenere il JSON originale
        parsed_content = json.loads(content_str)

        # Decodifica finale per ottenere la lista degli strumenti
        return json.loads(parsed_content)

    def simple_completion(self, query):
        payload = self._build_simple_payload(query)
        response = requests.post(f"{self.host}/api/chat", json=payload)
        result = response.json()
        return result["message"]["content"]

    def function_calling_completion(self, query, tools):
        payload = self._build_function_call_payload(query, tools)
        response = requests.post(f"{self.host}/api/chat", json=payload)
        result = response.json()
        return self._extract_content(result)

    def auto_completion(self, query, tools=None):
        if tools:
            return self.function_calling_completion(query, tools)
        else:
            return self.simple_completion(query)