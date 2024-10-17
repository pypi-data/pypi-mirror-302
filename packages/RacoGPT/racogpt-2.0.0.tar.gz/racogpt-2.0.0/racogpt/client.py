import requests
import json

class RacoGPTClient:
    def __init__(self, host="http://localhost:11434", model="RacoGPT"):
        self.host = host
        self.model = model
        self.history = []
        self.system_message = {
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
        }

    def _build_simple_payload(self, query, role="user"):
        return {
            "model": self.model,
            "messages": self.history + [{"role": role, "content": query}],
            "stream": False
        }

    def _build_function_call_payload(self, query, tools, role="user"):
        content = json.dumps({"query": query, "tools": tools})
        return {
            "model": self.model,
            "messages": self.history + [
                self.system_message,
                {"role": role, "content": content}
            ],
            "stream": False
        }

    def _extract_content(self, result):
        content_str = result["message"]["content"]
        try:
            parsed_content = json.loads(content_str)
            return json.loads(parsed_content)
        except (json.JSONDecodeError, TypeError):
            return content_str

    def simple_completion(self, query, role="user"):
        payload = self._build_simple_payload(query, role)
        response = requests.post(f"{self.host}/api/chat", json=payload)
        result = response.json()
        return result["message"]["content"]

    def function_calling_completion(self, query, tools, role="user"):
        payload = self._build_function_call_payload(query, tools, role)
        response = requests.post(f"{self.host}/api/chat", json=payload)
        result = response.json()
        return self._extract_content(result)

    def auto_completion(self, query, tools=None, role="user"):
        if tools:
            return self.function_calling_completion(query, tools, role)
        else:
            return self.simple_completion(query, role)

    def set_history(self, messages):
        self.history = messages

    @property
    def get_chat_history(self):
        return self.history

    def full_completion(self, messages, tools=None, role="user"):
        self.set_history(messages)
        if tools:
            # Update user messages with tools information and prepend the system message
            updated_messages = [
                {
                    "role": message["role"],
                    "content": json.dumps({"query": message["content"], "tools": tools}) if message["role"] == role else message["content"]
                }
                for message in messages
            ]
            updated_messages.insert(0, self.system_message)  # Prepend the system message

            # Prepare the payload with the updated messages
            payload = {
                "model": self.model,
                "messages": updated_messages,
                "stream": False
            }
            response = requests.post(f"{self.host}/api/chat", json=payload)
            result = response.json()
            return self._extract_content(result)
        else:
            # If no tools are specified, proceed as usual
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False
            }
            response = requests.post(f"{self.host}/api/chat", json=payload)
            result = response.json()
            return result["message"]["content"]