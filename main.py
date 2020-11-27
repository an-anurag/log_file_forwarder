# -*- coding: utf-8 -*-

import os
import re
import time
import socket

from config import conf

source_file = os.path.join(conf.read('OSSEC', 'file'))
source_log = open(source_file, 'rb')

# Find the size of the file and move to the end
st_results = os.stat(source_file)
st_size = st_results.st_size
source_log.seek(st_size)

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logger_host = conf.read('prod-logger-input', 'host')
logger_port = int(conf.read('prod-logger-input', 'port'))
event_pattern = re.compile(r'EVENT: "\[INIT\](.*)\[END\]";')

while True:
    where = source_log.tell()
    line = source_log.readline()
    if not line:
        time.sleep(1)
        source_log.seek(where)
    else:
        soc.sendto(bytes(line), (logger_host, logger_port))
