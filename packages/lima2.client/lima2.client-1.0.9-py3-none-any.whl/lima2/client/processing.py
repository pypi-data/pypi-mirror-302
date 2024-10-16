# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

"""Processing base class.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.
"""
from __future__ import annotations

import json
import logging
from jsonschema_default import create_from

import tango

from .convert import frame_info_to_shape_dtype

# Create a logger
_logger = logging.getLogger(__name__)


class ProcessingMetaclass(type):
    def __init__(self, name, bases, namespace, **kwargs):
        self.tango_db = None
        if "tango_class" in kwargs:
            self.tango_class = kwargs["tango_class"]

    @property
    def params_schema(self) -> dict:
        """
        Get the parameters's schema for the given tango_class
        """
        if not self.tango_db:
            self.tango_db = tango.Database()

        def get_schema(param):
            prop = self.tango_db.get_class_attribute_property(self.tango_class, param)
            # Each attribute property is a StdStringVector with a single value
            if param in prop:
                return json.loads(prop[param]["schema"][0])

        return get_schema("proc_params")

    @property
    def params_default(self) -> dict:
        """
        Returns a set of parameters with default values.
        """
        return create_from(self.params_schema)


class Processing(object, metaclass=ProcessingMetaclass):
    """A base class for all processings."""

    DEFAULT_TANGO_TIMEOUT = 20 * 60  #

    def __init__(
        self,
        uuid,
        proc_devs: list[str],
        timeout: int = DEFAULT_TANGO_TIMEOUT,
    ):
        """Construct a Processing object.

        Args:
            uuid: Unique identifer of the acquisition
            proc_devs: Variable length processing device instance names (aka domain/family/member)
            timeout: The tango device timeout [second]
            tango_class: The tango class of the device (aka LimaProcessingLegacy)

        """

        # Preconditions
        if not proc_devs:
            raise ValueError("Must provide at least one processing")

        self.__uuid = uuid

        self.__devs = [tango.DeviceProxy(r) for r in list(proc_devs)]
        for d in self.__devs:
            d.set_green_mode(tango.GreenMode.Gevent)
            d.set_timeout_millis(timeout * 1000)

        # self.__names = json.loads(self.__devs[0].progress_counters).keys()

    @property
    def uuid(self):
        """Return the UUID of the processing"""
        return self.__uuid

    @property
    def input_frame_info(self):
        """Return the dtype and shape of the input frame for each receivers"""
        return [
            frame_info_to_shape_dtype(json.loads(dev.input_frame_info))
            for dev in self.__devs
        ]

    @property
    def processed_frame_info(self):
        """Return the dtype and shape of the processed frame for each receivers"""
        return [
            frame_info_to_shape_dtype(json.loads(dev.processed_frame_info))
            for dev in self.__devs
        ]

    @property
    def progress_counters(self):
        """Returns the progress counters"""
        # Counter = namedtuple("Counter", self.__names)
        # return [Counter(**json.loads(dev.progress_counters)) for dev in self.__devs]
        return [json.loads(dev.progress_counters) for dev in self.__devs]

    def ping(self):
        """
        Ping all the devices of the system.

        Raises:
            tango.ConnectionFailed: if the connection failed.

        """
        for d in self.__devs:
            d.ping()

    @property
    def procs(self):
        return self.__devs

    @property
    def is_finished(self):
        """A list of `is_finished` for each devices."""
        return [dev.is_finished for dev in self.__devs]

    def register_on_finished(self, cbk):
        """
        Register a callback function to be notified on pipeline finish

        Arg:
            cbk: A callback `on_finished(evt: Tango.Event)` called for each receivers

        Returns:
            A dict mapping the processing instance name with the event id
        """

        return {
            proc: proc.subscribe_event(
                "is_finished", tango.EventType.DATA_READY_EVENT, cbk
            )
            for proc in self.__devs
        }

    @property
    def last_error(self):
        """A list of `last_error` for each devices."""
        return [dev.last_error for dev in self.__devs]

    def register_on_error(self, cbk):
        """
        Register a callback function to be notified on pipeline error

        Arg:
            cbk: A callback `on_error(evt: Tango.Event)` called for each receivers

        Returns:
            A dict mapping the processing instance name with the event id
        """

        return {
            proc: proc.subscribe_event(
                "last_error", tango.EventType.DATA_READY_EVENT, cbk
            )
            for proc in self.__devs
        }
