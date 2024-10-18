#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contains SpiceManager class to deal with spiceypy module.
"""
import os
import logging
from datetime import datetime, timedelta

import spiceypy

import spice_manager.constants as constants


__all__ = ['SpiceManager']


LOGGER = logging.getLogger(__file__)

class Singleton(type):
    """
    A metaclass to create singletons, i.e classes that can have at most only
    one instance created at a given time.
    """
    def __call__(cls, *args, **kwargs):
        """
        Check that an instance is already stored before creating a new one.
        """
        if hasattr(cls, 'instance'):
            return cls.instance

        cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance

    def clear(cls):
        cls._instance = None


class SpiceManager(metaclass=Singleton):
    """
    Spice Manager, adapted from Solar Orbiter SOC.
    Adapted from Solar Orbiter SOC
    Version: 1.0
    Date: 09-Aug-2016

    (see https://issues.cosmos.esa.int/solarorbiterwiki/display/SOSP/Translate+from+OBT+to+UTC+and+back)
    """

    # Include constants in the class directly
    SPICE_NAIF_ID = constants.NAIF_ID
    TIME_ISOC_STRFORMAT = constants.TIME_ISOC_STRFORMAT

    # Keep spiceypy inside class
    _spiceypy = spiceypy

    def __init__(self, spice_kernels=None,
                 logger=LOGGER):

        # Initialize attribute to stored loaded spice kernels
        self._kernels = []

        self.logger = logger

        # Load spice kernels
        if spice_kernels:
            self.kernels = spice_kernels

    @property
    def kernels(self):
        """
        Property for SPICE kernels

        :return: list of spice_kernels in self._kernels
        """
        return self._kernels

    @kernels.setter
    def kernels(self, spice_kernels):
        """
        Set self._kernels with input list of spice_kernels

        :param spice_kernels: list of input spice kernels to load
        :param append: If True, then append input list to the existing list in self._kernels. Otherwise the existing list in self._kernels will be replaced
        :return:
        """
        self.furnsh(spice_kernels)


    def furnsh(self, spice_kernels):
        """
        Load input spice kernels

        :param spice_kernels: list of spice kernels to load
        :return:
        """
        for kernel in spice_kernels:
            # Check if kernel exists
            if not os.path.isfile(kernel):
                self.logger.error(f'{kernel} not found, skip it!')
                continue
            else:
                kernel = os.path.abspath(kernel)

            # Only load new kernels
            if kernel not in self._kernels:
                self._kernels.append(kernel)
                spiceypy.furnsh(kernel)
                self.logger.info(f'{kernel} loaded')
            else:
                self.logger.debug(f'{kernel} already loaded')

    def unload(self, spice_kernels):
        """
        Unload input spice kernels

        :param spice_kernels: list of spice kernels to unload
        :return:
        """

        for kernel in spice_kernels.copy():
            if kernel in self._kernels:
                spiceypy.unload(kernel)
                self._kernels.remove(kernel)
                self.logger.info(f'{kernel} unloaded')
            else:
                self.logger.debug(f'{kernel} not loaded')

    def unload_all(self):
        """
        Unload all spice kernels.

        :return:
        """
        self.unload(self._kernels)

    @staticmethod
    def kall(kind='ALL'):
        """
        Return a dictionary of all kernels loaded

        :param kind – A list of kinds of kernels to return.
        :type str
        :return: list of loaded kernels
        """

        # Get number of loaded kernels
        count = spiceypy.ktotal(kind)

        kdict = {}
        for i in range(0, count):
            [ file, type, source, handle] = spiceypy.kdata(i, kind)
            kdict[os.path.basename(file)] = [ file, type, source, handle]

        return kdict


    @staticmethod
    def cuc2obt(cuc_time):
        """
        Convert input CCSDS CUC time into Spacecraft Clock string readable by spiceypy functions.

        :param cuc_time: 2-elements numpy array with coarse and fine parts of the CCSDS CUC time
        :return: Spacecraft Clock string
        """
        return f'1/{cuc_time[0]}:{cuc_time[1]}'

    @staticmethod
    def obt2cuc(obt_string):
        """
        Convert input Spacecraft Clock string into CCSDS CUC coarse and fine parts

        :param obt_string: input Spacecraft Clock string
        :return: 2-elements list containing CCSDS CUC coarse and fine part integers
        """
        items = obt_string[2:].split(':')

        coarse = None
        fine = None
        if len(items) == 2:
            coarse = int(items[0])
            fine = int(items[1])

        return coarse, fine

    @staticmethod
    def obt2et(naif_id, obt_string):
        # Spacecraft Clock to Ephemeris time (seconds past J2000)
        return spiceypy.scs2e(naif_id, obt_string)

    @staticmethod
    def et2obt(naif_id, ephemeris_time):
        # Ephemeris time to Spacecraft Clock
        return spiceypy.sce2s(naif_id, ephemeris_time)

    @staticmethod
    def et2utc(ephemeris_time, precision=6):
        """
        Convert input Spacecraft Clock string into UTC string

        :param ephemeris_time: input Ephemeris time
        :param precision: Digits of precision in fractional seconds
        :return: UTC string in ISO Calendar format
        """

        # Ephemeris time to UTC
        # Format of output epoch: ISOC (ISO Calendar format, UTC)
        # Digits of precision in fractional seconds: 6
        return spiceypy.et2utc(ephemeris_time, 'ISOC', precision)

    @staticmethod
    def obt2utc(naif_id, obt_string):
        """

        :param naif_id: NAIF ID of the observer/spacecraft
        :param obt_string: On-board time as string (e.g. "521651623:37539" or "1/0521651623:37539")
        :return: UTC time as string (e.g., "2016-194T15:13:46.381")
        """

        # Obt to Ephemeris time (seconds past J2000)
        ephemeris_time = spiceypy.scs2e(naif_id, obt_string)
        # Ephemeris time to Utc
        # Format of output epoch: ISOC (ISO Calendar format, UTC)
        # Digits of precision in fractional seconds: 3
        return spiceypy.et2utc(ephemeris_time, 'ISOC', 3)

    @staticmethod
    def utc2obt(naif_id, utc_string):
        """

        :param naif_id: NAIF ID of the observer/spacecraft
        :param utc_string: UTC time as a string (e.g., "2016-194T15:13:46.381")
        :return: on-board time as a string (e.g. "1/0521651623:37539")
        """

        # Utc to Ephemeris time (seconds past J2000)
        ephemeris_time = spiceypy.utc2et(utc_string)
        # Ephemeris time to Obt
        return spiceypy.sce2s(naif_id, ephemeris_time)

    @staticmethod
    def utc2et(utc_string):
        """
        Convert input UTC string into ephemeris time

        :param utc_string: UTC string in ISO Calendar format
        :return: ephemeris time
        """

        # Utc to Ephemeris time (seconds past J2000)
        return spiceypy.utc2et(utc_string)

    @staticmethod
    def et2tdt(ephemeris_time):
        """
        Convert input ephemeris time into Terrestrial Dynamical Time (TDT).

        :param ephemeris_time: input ephemeris time
        :return: Terrestrial Dynamical Time (TDT)
        """

        # Compute Terrestrial Dynamical Time (TDT)
        return spiceypy.unitim(ephemeris_time, 'ET', 'TDT')

    @staticmethod
    def tdt2utc(tdt_time):
        """
        Convert input TDT time into UTC time.

        :param tdt_time: input Terrestrial Dynamical Time (TDT)
        :return: UTC time
        """

        # Compute Ephemeris time (== TDB)
        et = spiceypy.unitim(tdt_time, 'TDT', 'ET')

        # return UTC
        return SpiceManager.et2utc(et)

    @staticmethod
    def utc_datetime_to_str(utc_datetime):
        """
        Convert an input UTC datetime as a string that can be
        passed to SPICE programs (e.g., utc2et)

        :param utc_datetime: datetime.datetime object containing utc time to convert
        :return: string with valid format for SPICE
        """

        return utc_datetime.strftime(SpiceManager.TIME_ISOC_STRFORMAT)

    @staticmethod
    def utc_str_to_datetime(utc_string):
        """
        Convert input UTC string into datetime.datetime object

        :param utc_string: UTC time as a string (e.g., "2016-194T15:13:46.381")
        :return: UTC as datetime.datetime object
        """
        return datetime.strptime(utc_string, SpiceManager.TIME_ISOC_STRFORMAT)

    def cuc2str(self, cuc_coarse_time, cuc_fine_time):
        """
        Convert input CCSDS CUC time into string "coarse:fine"

        :param cuc_coarse_time: integer containing the coarse part of the CCSDS CUC time
        :param cuc_fine_time: integer containing the fine part of the CCSDS CUC time
        :return: string with format "coarse:fine"
        """
        return '{0}:{1}'.format(cuc_coarse_time, cuc_fine_time)

    def cuc2datetime(self, cuc_coarse_time, cuc_fine_time,
                base_time=constants.RPW_TIME_BASE,
                cuc_fine_max=constants.CUC_FINE_MAX):
        """
        Convert input CCSDS CUC time into datetime.datetime object

        :param cuc_coarse_time: integer containing the coarse part of the CCSDS CUC time
        :param cuc_fine_time: integer containing the fine part of the CCSDS CUC time
        :param base_time: time origin used for computation (default is SOLO/RPW)
        :param cuc_fine_max: upper limit value of the CCSDS CUC fine
        :return: datetime.datetime object containing the input CCSDS CUC time
        """
        seconds_since_time_base = float(cuc_coarse_time) + (
                float(cuc_fine_time) / float(cuc_fine_max))
        return base_time + timedelta(seconds=seconds_since_time_base)
