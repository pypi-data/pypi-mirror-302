import ggps

import pytest

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_tcx_handler_2024.py


def expected_first_trackpoint():
    return {
        "type": "Trackpoint",
        "time": "2024-09-19T11:05:15.000Z",
        "latitudedegrees": 35.49427421763539,
        "longitudedegrees": -80.83952489309013,
        "altitudemeters": 249.1999969482422,
        "distancemeters": 0.8799999952316284,
        "heartratebpm": 68,
        "speed": 0.0,
        "cadence": 0,
        "watts": "0",
        "altitudefeet": 817.5852918249416,
        "distancemiles": 0.0005468066462059252,
        "distancekilometers": 0.0008799999952316285,
        "elapsedtime": "00:00:00",
        "seq": 1,
        "elapsedseconds": 0.0,
    }


def expected_last_trackpoint():
    return {
        "type": "Trackpoint",
        "time": "2024-09-19T11:51:32.000Z",
        "latitudedegrees": 35.49437488429248,
        "longitudedegrees": -80.840053120628,
        "altitudemeters": 244.1999969482422,
        "distancemeters": 8045.7001953125,
        "heartratebpm": 145,
        "speed": 3.171999931335449,
        "cadence": 90,
        "watts": "192",
        "altitudefeet": 801.1810923498758,
        "distancemiles": 4.9993663227454785,
        "distancekilometers": 8.0457001953125,
        "cadencex2": 180,
        "elapsedtime": "00:46:17",
        "seq": 2782,
        "elapsedseconds": 2777.0,
    }


def test_lorimer_avinger_tcx_file():
    expected_trackpoint_count = 2782
    filename = "data/activity_17075053124_lorimer_avinger.tcx"
    opts = dict()
    opts["run_walk_separator_cadence"] = 151
    handler = ggps.TcxHandler(opts)
    handler.parse(filename)

    helper = UnitTestHelper(handler)
    helper.assert_filename(filename)
    helper.assert_ggps_version()
    helper.assert_ggps_parsed_at()

    helper.assert_trackpoint_count(expected_trackpoint_count)
    helper.assert_first_trackpoint(expected_first_trackpoint())
    helper.assert_last_trackpoint(expected_last_trackpoint())
    helper.assert_str()

    assert (
        handler.get_data()["stats"]["cadence_data"]["run_walk_separator_cadence"] == 151
    )

    # test no-stats
    opts = dict()
    opts["no-stats"] = "any value"
    handler = ggps.TcxHandler(opts)
    handler.parse(filename)
    assert "stats" not in handler.get_data().keys()

    # test case of an invalid non-int run_walk_separator_cadence
    opts = dict()
    opts["run_walk_separator_cadence"] = "bad value!"
    handler = ggps.TcxHandler(opts)
    handler.parse(filename)
    assert (
        handler.get_data()["stats"]["cadence_data"]["run_walk_separator_cadence"] == 150
    )
