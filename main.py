# -*- coding: utf-8 -*-

from bundle.forwarder import Forwarder
from bundle.yaml_reader import get_sources_from_yaml

if __name__ == '__main__':

    LOG_SOURCES = get_sources_from_yaml()

    for source in LOG_SOURCES['log-sources']:
        name = source['name']
        log_file = source['path']
        file_type = source['file-type']
        host = source['host']
        port = source['port']
        socket_type = source['type']
        forwarder = Forwarder(name, log_file, file_type, host, port, socket_type)
        forwarder.create_socket()
        forwarder.run()
