import re
import uuid
import requests
from datetime import datetime


class TaxRequest:
    def __init__(self) -> None:
        self.return_content = None
        self.token = None
        self.timestamp = None
        self.json = {}
        self.content = ""

    def headers(self, token: bool = False) -> dict:
        headers = {
            "requestTraceId": str(uuid.uuid4()),
            "timestamp": str(int(datetime.now().timestamp() * 1000)) if not self.timestamp else self.timestamp,
        }
        if token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, url: str, data: dict, headers: dict = None, params: dict = None, verify: bool = True) -> dict:
        if not headers:
            headers = self.headers()
        res = requests.post(url, json=data, headers=headers, params=params, verify=verify)
        self.content = res.content.decode("utf-8")
        try:
            res.raise_for_status()
        except requests.HTTPError:
            if res.status_code == 400 and hasattr(res, "json"):
                pass
            else:
                if self.return_content:
                    return {"error": self.content}
                raise requests.HTTPError(self.content, response=res.status_code)
        if not hasattr(res, "json"):
            raise AttributeError("response has not json attribute")
        self.json = res.json()
        return self.json

    def get_content(self) -> str:
        return self.content.decode("utf-8")

    def response(self) -> dict:
        if isinstance(self.json, dict):
            result = {}
            for key, val in self.json.items():
                key = "_".join([i.lower() for i in re.split("(?<=.)(?=[A-Z])", key)])
                result[key] = val
        else:
            result = []
            for num, item in enumerate(self.json):
                keys = {}
                for key, val in item.items():
                    key = "_".join([i.lower() for i in re.split("(?<=.)(?=[A-Z])", key)])
                    keys[key] = val
                result.append(keys)
        return result
