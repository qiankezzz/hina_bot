# coding:utf-8
import json
import os
from pathlib import Path

path = Path() / 'data' / 'mazui_study' / 'resource' / 'mazui_state.json'
path.parent.mkdir(parents=True, exist_ok=True)
path = os.path.abspath(path)


class utils:

    @staticmethod
    def write_study(params: json) -> None:
        with open(f"{path}", 'w', encoding='utf-8') as f:
            json.dump(params, f, indent=4)

    @staticmethod
    def read_study(state: str) -> bool:
        if not os.path.exists(path):
            utils.write_study({
                'mazui_state':True
            })
        with open(f"{path}", 'r', encoding='utf-8') as f:
            now_state: json = json.load(f)
            state: bool = bool(now_state[state])

        return state

    @staticmethod
    def mod_json_data(state: str, value: bool) -> json:
        with open(f"{path}", 'r', encoding='utf-8') as f:
            params = json.load(f)

            params[state] = value

            return params

    @staticmethod
    def mod_json_data_dict(get_dict: dict) -> json:
        with open(f"{path}", 'r', encoding='utf-8') as f:
            params = json.load(f)

            for key in get_dict:
                value = get_dict[key]
                params[key] = value

            return params
