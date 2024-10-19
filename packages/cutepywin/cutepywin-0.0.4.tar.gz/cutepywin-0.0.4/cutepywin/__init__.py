import os
import re
import platform
from datetime import datetime


class Logger:
    """
    Logger class to handle different levels of logging.

    Methods:
        info(message: str) -> None:
            Logs an informational message.
        error(message: str) -> None:
            Logs an error message.
        system(message: str) -> None:
            Logs a system message.
        debug(message: str) -> None:
            Logs a debug message.
        api(message: str) -> None:
            Logs an API message.
    """

    @staticmethod
    def log(level: str, message: str) -> None:
        """
        General method to log messages with a specific log level.

        Args:
            level (str): The logging level (e.g., INF, ERR, SYS, DBG, API).
            message (str): The message to log.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"({level}): {timestamp} - {message}")

    @staticmethod
    def info(message: str) -> None:
        """
        Logs an informational message with the level (INF).
        
        Args:
            message (str): The information to log.
        """
        Logger.log("INF", message)

    @staticmethod
    def error(message: str) -> None:
        """
        Logs an error message with the level (ERR).
        
        Args:
            message (str): The error message to log.
        """
        Logger.log("ERR", message)

    @staticmethod
    def system(message: str) -> None:
        """
        Logs a system message with the level (SYS).
        
        Args:
            message (str): The system-related message to log.
        """
        Logger.log("SYS", message)

    @staticmethod
    def debug(message: str) -> None:
        """
        Logs a debug message with the level (DBG).
        
        Args:
            message (str): The debug message to log.
        """
        Logger.log("DBG", message)

    @staticmethod
    def api(message: str) -> None:
        """
        Logs an API message with the level (API).
        
        Args:
            message (str): The API-related message to log.
        """
        Logger.log("API", message)
        
    @staticmethod
    def msg(message: str) -> None:
        """
        Logs a message with the level (LOG).
        
        Args:
            message (str): The LOG-related message to log.
        """
        Logger.log("LOG", message)


class RGB():
    """
    Class to handle RGB color formatting for terminal output.
    
    Methods:
        print_color(r: int, g: int, b: int) -> str:
            Returns the ANSI escape code for RGB color.
    """
    reset = "\033[0m"
    def print(self, r: int, g: int, b: int) -> str:
        """
        Returns an ANSI escape code string for RGB color formatting.

        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).

        Returns:
            str: ANSI escape code for the specified RGB color.
        """
        return f"\033[38;2;{r};{g};{b}m"


class HEX():
    """
    Class to handle HEX color formatting for terminal output.
    
    Methods:
        print_color(hex_value: str) -> str:
            Returns the ANSI escape code for HEX color.
    """
    reset = "\033[0m"
    @staticmethod
    def print(hex_value: str) -> str:
        """
        Returns an ANSI escape code string for HEX color formatting.

        Args:
            hex_value (str): HEX color string (without the '#'), e.g., 'ff0000'.

        Returns:
            str: ANSI escape code for the specified HEX color.
        """
        hex_value = hex_value.lstrip("#")
        if not re.match(r"^[0-9A-Fa-f]{6}$", hex_value):
            raise ValueError(f"Invalid HEX color: {hex_value}")

        r, g, b = tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"


class Clear:
    """
    Utility class to clear the terminal screen.

    Methods:
        sys() -> None:
            Clears the terminal screen based on the operating system.
    """

    @staticmethod
    def sys() -> None:
        """
        Clears the terminal screen. Uses 'cls' for Windows and 'clear' for other systems.
        """
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')