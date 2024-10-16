# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT licence. See LICENSE for more info.

import logging
import gevent
import gevent.event
import json
import argparse
from functools import partial
from contextlib import ExitStack
from uuid import uuid1
from tango.gevent import DeviceProxy

from lima2.client import Detector, State
from lima2.client.pipelines.legacy import Processing

# Create a logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# Enable logging
logging.basicConfig()


def get_saving_groups(proc_params):
    return [g for n, g in proc_params.items() if n.startswith("sav")]


def run_acquisition(device, uuid, params: dict, cb={}):
    if uuid is None:
        uuid = uuid1()

    with ExitStack() as stack:
        not_running_event = gevent.event.Event()
        idle_event = gevent.event.Event()

        def state_cb(state):
            _logger.debug(f"State change to {state=}")
            state_cb = cb.get("state", None)
            if state_cb:
                state_cb(state)
            if state in [State.IDLE, State.FAULT]:
                _logger.debug("Setting not_running_event")
                not_running_event.set()
            if state == State.IDLE:
                _logger.debug("Setting not_running_event")
                idle_event.set()

        device.register_transition_logger(state_cb)
        stack.callback(partial(device.unregister_transition_logger, state_cb))

        device.prepare_acq(
            uuid, params["ctrl_params"], params["recv_params"], params["proc_params"]
        )
        # stack.callback(partial(device.erase_pipeline, uuid))
        # proc = stack.enter_context(device.get_pipeline(uuid))
        proc = device.get_pipeline(uuid)
        prepare_cb = cb.get("prepare", None)
        if prepare_cb:
            prepare_cb(uuid, proc)

        end_cb = cb.get("end", None)
        if end_cb:
            stack.callback(end_cb)

        for e in [not_running_event, idle_event]:
            e.clear()

        device.start_acq()
        start_cb = cb.get("start", None)
        if start_cb:
            start_cb()

        def stop_wait_proc():
            # Stop if running
            if device.state == State.RUNNING:
                _logger.info("Stopping running acquisition ...")
                device.stop_acq()
            if device.state == State.CLOSING:
                while not idle_event.ready():
                    idle_event.wait(1.0)
            # Signal that acq has stopped
            stop_cb = cb.get("stop", None)
            if stop_cb:
                stop_cb(device.nb_frames_xferred)
            # Wait for the end of the processing
            while not proc.is_finished:
                gevent.sleep(0.1)

        stack.callback(stop_wait_proc)

        while not not_running_event.ready():
            xfer_cb = cb.get("xfer", None)
            if xfer_cb:
                xfer_cb(device.nb_frames_xferred)
            not_running_event.wait(1.0)


class Acquisition:
    def __init__(self, device, args, params):
        self.device = device
        self.args = args

        self.acq_params = params["acq_params"]
        self.proc_params = params["proc_params"]

        self.start_event = gevent.event.Event()
        self.end_event = gevent.event.Event()
        self.xferred_frames = gevent.event.AsyncResult()
        self.uuid = self.args.get("uuid", None)
        self.proc = None

    def run(self):
        self.show_state("Run")

        params = {
            "ctrl_params": self.acq_params,
            "recv_params": [self.acq_params for _ in self.device.recvs],
            "proc_params": [self.proc_params for _ in self.device.recvs],
        }

        cb = dict(
            state=self.state_cb,
            prepare=self.prepare_cb,
            start=self.start_cb,
            xfer=self.xfer_cb,
            stop=self.stop_cb,
            end=self.end_cb,
        )

        return run_acquisition(self.device, self.uuid, params, cb)

    def show_state(self, name):
        _logger.info(f'{name + ":":8s} state={self.device.state}')

    def state_cb(self, state):
        if state is not None:
            _logger.info(f"Monitor: state={state}")
        else:
            _logger.info("\nMonitor finished!")

    def reading_loop(self, proc):
        self.start_event.wait()

        roi_counters = []

        def pop_roi_counters(progress_counters):
            # ROI counter acquisition
            n = min([c["nb_frames_counters"] for c in progress_counters])
            avail_frames = max(0, n - len(roi_counters))
            if avail_frames > 0:
                rc = proc.popRoiCounters(avail_frames)
                if rc:
                    roi_counters.append(rc)
            return avail_frames

        # Read the ROI statistics if enabled
        if self.proc_params["statistics"]["enabled"]:
            while not (self.end_event.ready() or proc.is_finished):
                progress_counters = proc.progress_counters
                _logger.info(f"Progress={progress_counters}")
                if self.proc_params["statistics"]["enabled"]:
                    pop_roi_counters(progress_counters)
                gevent.sleep(1)
            progress_counters = proc.progress_counters
            _logger.info(f"Final counters={progress_counters}")
            # Finish ROI counter download
            while pop_roi_counters(progress_counters):
                progress_counters = proc.progress_counters
            _logger.info(f"ROI Statistics={roi_counters}")

        # nb_frames_xferred = self.xferred_frames.get()
        # while True:
        #     try:
        #         frame = proc.getFrame(nb_frames_xferred - 1)
        #         break
        #     except:
        #         gevent.sleep(0.1)
        # print(f'Frame={frame}')

    def prepare_cb(self, uuid, proc):
        self.uuid = uuid
        _logger.info(f"UUID={uuid}")
        self.show_state("Prepare")
        self.proc = gevent.spawn(self.reading_loop, proc)

    def start_cb(self):
        self.show_state("Start")
        self.start_event.set()

    def xfer_cb(self, nb_frames_xferred):
        state = self.device.state
        _logger.info(f"Curr. {nb_frames_xferred=} {state=}")

        # Simulate an asynchronous Stop, if requested
        stop_frames = self.args.get("stop_after_nb_frames", 0)
        if (
            stop_frames
            and nb_frames_xferred >= stop_frames
            and self.device.state == State.RUNNING
        ):
            _logger.info("##### STOP #####")
            self.device.stopAcq()

    def stop_cb(self, nb_frames_xferred):
        self.show_state("Stop")
        _logger.info(f"Total {nb_frames_xferred=}")
        self.xferred_frames.set(nb_frames_xferred)

    def end_cb(self):
        self.show_state("End")
        self.end_event.set()
        self.proc.join()


def test_acquisition(device, args, params):
    print("*** Running acquisition ***")
    test = Acquisition(device, args.__dict__, params)
    test.run()


def pretty_print_json(json_str, desc=None):
    if desc:
        print(f"{desc}:")
    parsed = json.loads(json_str)
    print(json.dumps(parsed, indent=4, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description="Lima2 Client test program.")
    parser.add_argument("tango_ctrl_url", nargs=1, help="control Tango device name")
    parser.add_argument(
        "tango_recv_urls", nargs="+", help="receiver Tango device name(s)"
    )
    parser.add_argument("--acq_params", help="JSON string with acq_params")
    parser.add_argument("--uuid", help="Acquisition UUID")
    parser.add_argument(
        "--acq_params_file", help="file containg JSON string with acq_params"
    )
    parser.add_argument("--proc_params", help="JSON string with proc_params")
    parser.add_argument(
        "--proc_params_file", help="file containg JSON string with proc_params"
    )
    parser.add_argument(
        "--stop_after_nb_frames",
        type=int,
        help="Stop after a number of frames have been xferred",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print extra information useful for debbuging",
        action="store_true",
    )

    args = parser.parse_args()

    # Note that nargs=1 produces a list of one item
    tango_ctrl_url = args.tango_ctrl_url[0]
    tango_recv_urls = args.tango_recv_urls

    tango_ctrl_dev = DeviceProxy(tango_ctrl_url)
    tango_recv_devs = [DeviceProxy(url) for url in tango_recv_urls]
    device = Detector(tango_ctrl_dev, *tango_recv_devs)

    # Create the user data structures to set detector params
    acq_params = device.params_default[tango_ctrl_url]["acq_params"]

    proc_params = Processing.params_default
    proc_params["class_name"] = Processing.tango_class

    # Fill the params with the default params
    params = {"acq_params": acq_params, "proc_params": proc_params}

    def merge(a: dict, b: dict, path=[]):
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    # Fill the params either from command line or file
    params_keys = ["acq_params", "proc_params"]
    for key in params_keys:
        val = None
        val_str = getattr(args, key)
        if val_str:
            val = val_str
        fname = getattr(args, f"{key}_file")
        if fname:
            with open(fname) as f:
                val = f.read()
        if val:
            # Merge the default and command line / file args
            merge(params[key], json.loads(val))

    # Pretty print params
    if args.verbose:
        import pprint

        pprint.pprint(params)

    test_acquisition(device, args, params)

    input("Press Enter to close")


if __name__ == "__main__":
    t = gevent.spawn(main)
    t.join()
    print("Good bye!")
