#!/bin/bash

# Usage: send_result.sh /path/to/report.dcm
storescu 127.0.0.1 4242 -v -aec HIPPOAI "$1"