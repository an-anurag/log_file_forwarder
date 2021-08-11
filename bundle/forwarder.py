import os
import time
import socket
import threading

from bundle.logger import logger


class Forwarder(threading.Thread):
    log = logger

    def __init__(self, name=None, log_file=None, file_type=None, host=None, port=None, socket_type=None):
        super().__init__()
        self.name = name
        self.log_file = os.path.join(log_file)
        self.file_type = file_type
        self.host = host
        self.port = port
        self.socket_type = socket_type

        self.server = (self.host, self.port)
        self.socket = None

        self.log_file_ok = True
        if not os.path.exists(self.log_file):
            self.log_file_ok = False
            self.log.error("'{}' Log file does not exist".format(self.log_file))

    def create_socket(self):
        try:
            if self.socket_type == 'UDP':
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            if self.socket_type == 'TCP':
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            self.log.exception('Failed to create socket')

    def process_file(self):
        log = self.log
        if self.file_type == 'live':
            log.info('file processing started: %s' % self.name)
            log.info('Selected log source: %s' % self.log_file)
            log.info('Selected log file type is: %s' % self.file_type)
            log.info('Selected socket type: %s' % self.socket_type)
            log.info('Receiver host: %s' % self.host)
            log.info('Receiver port: %s' % self.port)

            if self.log_file_ok:
                source_file = self.log_file
                source_log = None

                try:
                    source_log = open(self.log_file, 'rb')
                    # Find the size of the file and move to the end
                    st_results = os.stat(source_file)
                    st_size = st_results.st_size
                    source_log.seek(st_size)
                except FileNotFoundError as err:
                    log.error('no "%s" log file found terminating the operation' % self.name)

                if source_log:
                    while True:
                        where = source_log.tell()
                        line = source_log.readline()
                        if not line:
                            log.info('waiting for log..')
                            time.sleep(1)
                            source_log.seek(where)
                        else:
                            self.socket.sendto(bytes(line), self.server)
                            log.info("log data sent: %s" % line)

        if self.file_type == 'static':
            log.info('file processing started: %s' % self.name)
            log.info('selected log source: %s' % self.log_file)
            log.info('Selected log file type is: %s' % self.file_type)
            log.info('selected socket type: %s' % self.socket_type)
            log.info('receiver host: %s' % self.host)
            log.info('receiver port: %s' % self.port)
            with open(self.log_file, 'r') as log_file:
                for line in log_file:
                    self.socket.sendto(bytes(line), self.server)
                    log.info("log data sent: %s" % line)

    def run(self) -> None:
        self.process_file()
