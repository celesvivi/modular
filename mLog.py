import os, datetime, sys
from enum import Enum
class TypeOfLog(Enum):
    INFO = 1
    ACTION = 2
    ERROR = 3

def get_app_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
# VERION 1.2
class Logger:
    """
    Logger class for logging
    Args:
        file_path (path, default = app_dir): dir of the log file 
        name (str, default = log.txt): name of log file
    """
    def __init__(self, file_path = None, name = None):
        if file_path is None:
            log_dir = self.get_app_directory()
        else:   
            log_dir = file_path
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

        if name is None:
            file_name = "log.txt"
        else: 
            file_name = name
            if not os.path.splitext(file_name)[1]:
                file_name += ".txt"
        
        self.log_path = os.path.join(log_dir, file_name)
        #Check if log file already exist
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', encoding = "utf-8") as f:
                f.write("Log created\n")


    def log(self, message, log_type = None): 
        """
        Write log to file
        Args:
            message (str): content
            log_type(int/TypeOfLog, default = 4/unknown): 1/info - 2/action - 3/error
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(log_type, TypeOfLog):
            log_type = log_type.value

        match log_type:
            case 1:
                log_entry = f"[{timestamp}] INFO: {message}\n"
            case 2:
                log_entry = f"[{timestamp}] DO: {message}\n"
            case 3: 
                log_entry = f"[{timestamp}] ERROR: {message}\n"
            case _:
                log_entry = f"[{timestamp}] UNKNOWN: {message}\n"
        with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)