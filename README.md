# Realtime log file forwarder

# What is this
This module reads any live .log file and send each newly appending line to web sockets in realtime.
All the files that needs to be sent should be configured in the log_sources.yaml file.

This module support live log files and static/offline log files as well

# How to run
- Run the `python main.py` to have all the files being sent to the syslog port
- This module can be kept running in the background with unix utility such as `screen`
