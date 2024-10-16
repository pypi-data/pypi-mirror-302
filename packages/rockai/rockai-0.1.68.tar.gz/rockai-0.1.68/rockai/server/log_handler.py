import logging

# Create a custom logging handler
class PrintLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_message = ""
    def emit(self, record):
        self.log_message += self.format(record)
    def get_log_msg(self):
        return self.log_message
    def clear_log_msg(self):
        self.log_message = ""

# Set up the logging configuration
def setup_logging():
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(logging.DEBUG)

    print_handler = PrintLoggingHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    print_handler.setFormatter(formatter)
    
    # Clear existing handlers to avoid duplicate logs
    # if logger.hasHandlers():
    #     logger.handlers.clear()
    
    logger.addHandler(print_handler)