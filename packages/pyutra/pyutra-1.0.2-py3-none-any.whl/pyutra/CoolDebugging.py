import os
from pyutra.ColorText import ColorText
from datetime import datetime

cool_text = ColorText()

class CoolDebugging:
    def __init__(self, log_file:str=None, color_config=None, watermark:bool=True, say_time:bool=True, silent:bool=True):
        if color_config is None:
            self.color_config = {
                "info": "cyan",
                "error": "red",
                "warning": "yellow",
                "success": "green"
            }
        self.silent = silent
        self.say_time = say_time
        self.log_file = log_file
        if log_file != None:
            now = datetime.now()

            time_cool = now.strftime("%m/%d/%Y %H:%M:%S")
            if not os.path.exists(log_file):
                with open(log_file, "w+") as f:
                    if watermark == True:
                        f.write("===== PyUltra by TheDiamondOG =====\n")
                    if say_time == True:
                        f.write(f"===== Log Start: {time_cool} =====\n")
            else:
                with open(log_file, "a") as f:
                    if say_time == True:
                        f.write(f"===== Log Start: {time_cool} =====\n")

    def info(self, message:str):
        if self.silent == False:
            print(cool_text.colorize(f"INFO: {message}", self.color_config["info"]))
        if self.log_file != None:
            with open(self.log_file, "a") as f:
                if self.say_time == True:
                    now = datetime.now()
                    time_cool = now.strftime("%m/%d/%Y %H:%M:%S")
                    f.write(f"\nINFO ({time_cool}): {message}")
                else:
                    f.write(f"\nINFO: {message}")

    def error(self, message:str):
        if self.silent == False:
            print(cool_text.colorize(f"ERROR: {message}", self.color_config["error"]))
        if self.log_file != None:
            with open(self.log_file, "a") as f:
                if self.say_time == True:
                    now = datetime.now()
                    time_cool = now.strftime("%m/%d/%Y %H:%M:%S")
                    f.write(f"\nERROR ({time_cool}): {message}")
                else:
                    f.write(f"\nERROR: {message}")

    def warning(self, message:str):
        if self.silent == False:
            print(cool_text.colorize(f"WARNING: {message}", self.color_config["warning"]))
        if self.log_file != None:
            with open(self.log_file, "a") as f:
                if self.say_time == True:
                    now = datetime.now()
                    time_cool = now.strftime("%m/%d/%Y %H:%M:%S")
                    f.write(f"\nWARNING ({time_cool}): {message}")
                else:
                    f.write(f"\nWARNING: {message}")

    def success(self, message:str):
        if self.silent == False:
            print(cool_text.colorize(f"SUCCESS: {message}", self.color_config["success"]))
        if self.log_file != None:
            with open(self.log_file, "a") as f:
                if self.say_time == True:
                    now = datetime.now()
                    time_cool = now.strftime("%m/%d/%Y %H:%M:%S")
                    f.write(f"\nSUCCESS ({time_cool}): {message}")
                else:
                    f.write(f"\nSUCCESS: {message}")