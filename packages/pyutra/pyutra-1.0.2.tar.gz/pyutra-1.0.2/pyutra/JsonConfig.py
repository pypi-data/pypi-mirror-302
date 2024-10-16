import json
import os
from pyutra.CoolDebugging import CoolDebugging

class JsonConfig:
    def __init__(self, file:str="config.json", default_config:dict=None, readable:bool=True, debug:bool=False):
        self.cool_debugging = CoolDebugging(silent=debug)
        if default_config == None:
            default_config = {"PLEASE SET DEFAULT CONFIG"}
            self.cool_debugging.error("Default config was not sent, the config system will not work well without it.")
        if not os.path.exists(file):
            self.cool_debugging.info("Config has not been made yet.")
            with open(file, "w+") as f:
                if readable == True:
                    json.dump(default_config, f, indent=4)
                    self.cool_debugging.info("Created config, the config is readable.")
                else:
                    json.dump(default_config, f)
                    self.cool_debugging.info("Created config")
        self.debug = debug
        self.file = file
        self.default_config = default_config
        self.readable = readable

    def read(self):
        with open(self.file, "r") as f:
            self.cool_debugging.info("Opened config file")
            data = json.load(f)
            self.cool_debugging.success(f"Loaded config data: {data}")
            return data

    def write(self, data:dict):
        with open(self.file, "w+") as f:
            self.cool_debugging.info(f"Attempting to write to config: {data}")
            json.dump(data, f)
            self.cool_debugging.success(f"Writen to config")

    def reset(self):
        with open(self.file, "w+") as f:
            self.cool_debugging.info(f"Attempting to reset config")
            json.dump(self.default_config, f)
            self.cool_debugging.success(f"Successfully reset config")

class EasyJsonConfig:
    def __init__(self, file:str="config.json", default_config:dict=None, readable:bool=True, debug:bool=False):
        self.cool_debugging = CoolDebugging(silent=debug)
        if default_config == None:
            default_config = {"PLEASE SET DEFAULT CONFIG"}
            self.cool_debugging.error("Default config was not sent, the config system will not work well without it.")
        if not os.path.exists(file):
            self.cool_debugging.info("Config has not been made yet.")
            with open(file, "w+") as f:
                if readable == True:
                    json.dump(default_config, f, indent=4)
                    self.cool_debugging.info("Created config, the config is readable.")
                else:
                    json.dump(default_config, f)
                    self.cool_debugging.info("Created config")
        self.debug = debug
        self.file = file
        self.default_config = default_config
        self.readable = readable

    def read(self, key:str):
        with open(self.file, "r") as f:
            self.cool_debugging.info("Opened config file")
            data = json.load(f)
            self.cool_debugging.success(f"Loaded config data: {data}")

        if "/" in key:
            last_data = data
            path = key.split("/")

            for i in path:
                last_data = last_data.get(i)
                if last_data is None:
                    return None
            return last_data
        else:
            return data.get(key)


    def write(self, key:str, value:str):
        with open(self.file, "r") as f:
            data = json.load(f)

        if "/" in key:
            last_data = data
            path = key.split("/")

            for i in path[:-1]:
                if i not in last_data:
                    last_data[i] = {}
                last_data = last_data[i]

            last_data[path[-1]] = value
        else:
            data[key] = value

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def reset(self):
        with open(self.file, "w+") as f:
            self.cool_debugging.info(f"Attempting to reset config")
            json.dump(self.default_config, f)
            self.cool_debugging.success(f"Successfully reset config")