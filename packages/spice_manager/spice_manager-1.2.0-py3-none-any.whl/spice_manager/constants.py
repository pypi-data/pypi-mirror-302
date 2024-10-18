#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Global variables for SPICE manager
"""

from datetime import datetime

__all__ = ['NAIF_ID', 'TIME_ISOC_STRFORMAT', 'RPW_TIME_BASE', 'CUC_FINE_MAX']

# List of NAIF SPICE IDs
NAIF_ID = {
    'SOLAR_ORBITER':-144,
    }


TIME_ISOC_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f'

# RPW time base
RPW_TIME_BASE = datetime(2000, 1, 1, 0, 0)

# CUC fine part max value
CUC_FINE_MAX = 65536
