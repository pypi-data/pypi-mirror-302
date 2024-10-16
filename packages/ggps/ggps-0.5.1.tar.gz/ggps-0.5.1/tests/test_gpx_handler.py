import ggps

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_gpx_handler.py


def expected_first_trackpoint():
    return {
        "type": "Trackpoint",
        "latitudedegrees": 44.97431952506304,
        "longitudedegrees": -93.26310088858008,
        "time": "2014-10-05T13:07:53.000Z",
        "heartratebpm": 85,
        "elapsedtime": "00:00:00",
        "elapsedseconds": 0.0,
        "seq": 1,
    }


def expected_trackpoint_1200():
    return {
        "type": "Trackpoint",
        "latitudedegrees": 44.91043584421277,
        "longitudedegrees": -93.2357053924352,
        "time": "2014-10-05T15:15:47.000Z",
        "heartratebpm": 140,
        "elapsedtime": "02:07:54",
        "elapsedseconds": 7674.0,
        "seq": 1200,
    }


def expected_last_trackpoint():
    return {
        "type": "Trackpoint",
        "latitudedegrees": 44.95180849917233,
        "longitudedegrees": -93.10493202880025,
        "time": "2014-10-05T17:22:17.000Z",
        "heartratebpm": 161,
        "elapsedtime": "04:14:24",
        "elapsedseconds": 15264.0,
        "seq": 2256,
    }


def test_twin_cities_marathon_gpx_file():
    expected_trackpoint_count = 2256
    filename = "data/twin_cities_marathon.gpx"
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
    helper.assert_trackpoint_at_index(expected_trackpoint_1200(), 1199)
    helper.assert_str()
