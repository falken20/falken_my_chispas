# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/logger.py

import sys
import os
from rich.console import Console
from rich.style import Style
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv())

# Create console object for logs
console = Console()

style_DEBUG = Style(color="cyan")  # style_debug = "red bold"
style_INFO = Style(color="green")
style_WARNING = Style(color="orange3", bold=True)
style_ERROR = Style(color="red", bgcolor="white", bold=True)

# Min log level to print
LEVEL_LOG = os.getenv('LEVEL_LOG', "DEBUG, INFO, WARNING, ERROR")
console.print(f"LOG LEVEL: {LEVEL_LOG}", style="yellow")


class Log():
    @staticmethod
    def debug(message, style=style_DEBUG):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.debug.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    @staticmethod
    def info(message, style=style_INFO):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.info.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    @staticmethod
    def warning(message, style=style_WARNING):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.warning.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    @staticmethod
    def error(message, err, sys, style=style_ERROR):
        """
        Print error in terminal
        Args:
            message: Messsage to show
            err(Exception): Exception
            sys(sys): System var
        """
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.error.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.rule("ERROR")
                console.print(time, level, message,
                              f"\nLine: {sys.exc_info()[2].tb_lineno} {type(err).__name__} ",
                              f"\nMethod: {sys.exc_info()[2].tb_frame.f_code.co_name} ",
                              f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} ",
                              f"\nError: {format(err)}",
                              style=style)

        except Exception as err:
            Log.error("Error to print log", err, sys)
