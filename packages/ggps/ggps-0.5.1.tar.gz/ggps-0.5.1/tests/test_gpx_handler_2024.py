import ggps

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_gpx_handler_2024.py


def expected_first_trackpoint():
    return {
        "type": "Trackpoint",
        "latitudedegrees": 35.49427421763539,
        "longitudedegrees": -80.83952489309013,
        "time": "2024-09-19T11:05:15.000Z",
        "heartratebpm": 68,
        "cadence": 0,
        "trackpointextension": "",
        "elapsedtime": "00:00:00",
        "elapsedseconds": 0.0,
        "seq": 1,
    }


def expected_last_trackpoint():
    return {
        "type": "Trackpoint",
        "latitudedegrees": 35.49437488429248,
        "longitudedegrees": -80.840053120628,
        "time": "2024-09-19T11:51:32.000Z",
        "heartratebpm": 145,
        "cadence": 90,
        "trackpointextension": "",
        "elapsedtime": "00:46:17",
        "cadencex2": 180,
        "elapsedseconds": 2777.0,
        "seq": 2778,
    }


def test_lorimer_avinger_gpx_file():
    expected_trackpoint_count = 2778
    filename = "data/activity_17075053124_lorimer_avinger.gpx"
    options = dict()
    handler = ggps.GpxHandler(options)
    handler.parse(filename)

    helper = UnitTestHelper(handler)
    helper.assert_filename(filename)
    helper.assert_ggps_version()
    helper.assert_ggps_parsed_at()

    helper.assert_trackpoint_count(expected_trackpoint_count)
    helper.assert_first_trackpoint(expected_first_trackpoint())
    helper.assert_last_trackpoint(expected_last_trackpoint())
    helper.assert_str()
