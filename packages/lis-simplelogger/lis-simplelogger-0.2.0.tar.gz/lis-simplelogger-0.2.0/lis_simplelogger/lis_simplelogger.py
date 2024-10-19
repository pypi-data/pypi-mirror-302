import logging
import logging.handlers


class LISSimpleLogger:

    '''
        LIS Simple Logger is a simple logging package that
        enables a user to easily see logs from the console
        and leave logs on a file simultaneously
    '''

    def __init__(self,log_file,logger_name):
        self.log_file = log_file
        self.logger_name = logger_name
        self.file_logger = None
        self.console_logger = None
    
    def set_logfile_path(self,path):
        self.log_file = path

    def full_setup(self):
        self.setup_file_logger()
        self.setup_console_logger()

    ''' 
                About Logger
        * Logger struct : Logger(Handler(Formatter))
        * logging module has internal dictionary that stores Logger objects.
    '''
    

    def setup_file_logger(self):
        self.file_logger = logging.getLogger(f'{self.logger_name}_file_logger')
        self.file_logger.setLevel(logging.DEBUG)
        file_handler = logging.handlers.RotatingFileHandler(self.log_file, maxBytes=10*1024*1024, backupCount=10000) # sufficient amount of backups
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.file_logger.addHandler(file_handler)
    
    def setup_console_logger(self):
        self.console_logger = logging.getLogger(f'{self.logger_name}_console_logger')
        self.console_logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
        stream_handler.setFormatter(stream_formatter)
        self.console_logger.addHandler(stream_handler)

    
    def get_file_logger(self):
        return self.file_logger
    
    def get_console_logger(self):
        return self.console_logger

    def info_log(self,msg):
        self.file_logger.info(msg)
        self.console_logger.info(msg)

    def warning_log(self,msg):
        self.file_logger.warning(msg)
        self.console_logger.warning(msg)

    def error_log(self,msg):
        self.file_logger.error(msg)
        self.console_logger.error(msg)
        
    def critical_log(self,msg):
        self.file_logger.critical(msg)
        self.console_logger.critical(msg)
