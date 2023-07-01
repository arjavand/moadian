import json
from typing import List, Union


class JSONNormalizer:
    @staticmethod
    def hex_string_to_byte_array(s: str) -> bytes:
        data = bytes.fromhex(s)
        return data

    @staticmethod
    def get_key(root_key: str, my_key: str) -> str:
        if root_key is not None:
            return f"{root_key}.{my_key}"
        else:
            return my_key

    def normal_json(self, obj: Union[str, List[object], dict], headers: Union[dict, None] = None) -> Union[str, None]:
        if headers is None:
            headers = {}
        if obj is None and headers is None:
            return None
        data = obj
        if isinstance(obj, str):
            try:
                data = json.loads(obj)
            except json.JSONDecodeError as e:
                raise RuntimeError(str(e))
        if isinstance(data, list):
            packets_wrapper = {"packets": data}
            map_data = packets_wrapper
        else:
            map_data = data
        if headers is not None:
            for key, val in headers.items():
                if key and key == "Authorization":
                    map_data.update({key: val[7:]})
                else:
                    map_data.update({key: val})
        result = {}
        self.flat_map(result, None, map_data)
        keys = sorted(result.keys())
        output = []
        for key in keys:
            value = result[key]
            if value is not None:
                text_value = str(value)
                if text_value == "" or text_value is None:
                    text_value = "#"
                else:
                    text_value = text_value.replace("#", "##")
            else:
                text_value = "#"
            output.append(text_value)
        return "#".join(output)

    def flat_map(self, result: dict, root_key: Union[str, None], input_data: Union[list, dict, object]) -> None:
        if isinstance(input_data, list):
            for i, element in enumerate(input_data):
                key = self.get_key(root_key, f"E{i}")
                self.flat_map(result, key, element)
        elif isinstance(input_data, dict):
            for key, value in input_data.items():
                key = self.get_key(root_key, key)
                self.flat_map(result, key, value)
        else:
            result[root_key] = input_data
