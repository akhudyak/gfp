import os
import logging
from datetime import datetime
from gfp_configuration import GfpConfig


class GfpServer:
    def __init__(self):
        # self.handle_log()
        self.config = GfpConfig()

    def handle_log(self):
        log_filename = f"gfp_logging_{datetime.now().strftime('%Y%m%d-%H%M%S.%f')}.txt"
        log_file_path = os.path.join("logs", log_filename)
        log_format = "%(asctime)s - %(threadName)s: %(levelname)s: %(message)s | Line:%(lineno)d at %(module)s:%(funcName)s"
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.mkdir(os.path.dirname(log_file_path))
        logging.basicConfig(filename=log_file_path,
                            level=logging.INFO, filemode='w', format=log_format)
        