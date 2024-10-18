#! /usr/bin/env python3
# -*- coding:Utf8 -*-

import os.path as osp
import logging
from datetime import datetime

__all__ = ["ROOT_DIR", "SCOS_HEADER_BYTES",
           "LOGGER", "INPUT_STRFTIME",
           "INVALID_UTC_DATETIME", "INVALID_UTC_TIME",
           "TCREPORT_STRTFORMAT"]


ROOT_DIR = osp.dirname(osp.abspath(__file__))

# logger
LOGGER = logging.getLogger("edds_process")

# byte offset for the SCOS2000 header in DDS file
SCOS_HEADER_BYTES = 76

# Input string time format for datetime
INPUT_STRFTIME = "%Y-%m-%dT%H:%M:%S.%fZ"

# TC report time format
TCREPORT_STRTFORMAT = "%Y-%m-%dT%H:%M:%S.%f"

# value for invalid UTC Time
INVALID_UTC_TIME = '2000-01-01T00:00:00.000000'
INVALID_UTC_DATETIME = datetime.strptime(INVALID_UTC_TIME,
                                        TCREPORT_STRTFORMAT)
