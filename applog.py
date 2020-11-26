from flask import request
import logging
import arrow


class AppLog:

    def __init__(self):
        self.logger = logging.getLogger('waitress')
        self.logger.setLevel(logging.INFO)
        return

    def log_request(self,req: request = None):
        if req == None:
            return

        msg = '%s - %s - %s ' % (req.remote_addr, arrow.now().strftime("%Y/%m/%d %H:%M:%S"), req.url)
        print(msg)
        return

