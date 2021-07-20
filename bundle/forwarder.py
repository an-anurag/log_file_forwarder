import os
import time
import socket
import threading

from bundle.config import conf
from bundle.logger import logger
from bundle.yaml_reader import get_sources_from_yaml


class Forwarder:

    # socket info
    SOC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    HOST = conf.read('graylog-input', 'host')
    # to read socket port from cfg file
    # PORT = int(conf.read('graylog-input', 'port'))
    # SERVER = (HOST, PORT)
    LOGGER = logger

    # get log sources form path
    LOG_SOURCES = get_sources_from_yaml()

    def process_file(self, file, port):
        self.LOGGER.info('file processing started')
        self.LOGGER.info('file name: %s' % file)
        self.LOGGER.info('Selected socket type: UDP, port: %s' % port)
        source_file = os.path.join(file)
        source_log = None
        server = (self.HOST, int(port))

        try:
            source_log = open(source_file, 'rb')
        except FileNotFoundError as err:
            self.LOGGER.error(err)

        # Find the size of the file and move to the end
        st_results = os.stat(source_file)
        st_size = st_results.st_size
        source_log.seek(st_size)

        while True:
            where = source_log.tell()
            line = source_log.readline()
            if not line:
                time.sleep(1)
                source_log.seek(where)
            else:
                self.SOC.sendto(bytes(line), server)

    def run(self):
        # process all files parallelly
        for source in self.LOG_SOURCES['log-sources']:
            file_path = source['path']
            port = source['port']
            thread = threading.Thread(target=self.process_file, args=(file_path, port))
            thread.start()
