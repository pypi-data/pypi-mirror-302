import ggps

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_tcx_handler.py


def expected_first_trackpoint():
    return {
        "type": "Trackpoint",
        "time": "2014-10-05T13:07:53.000Z",
        "latitudedegrees": 44.97431952506304,
        "longitudedegrees": -93.26310088858008,
        "altitudemeters": 259.20001220703125,
        "distancemeters": 0.0,
        "heartratebpm": 85,
        "speed": 0.0,
        "cadence": 89,
        "altitudefeet": 850.3937408367167,
        "distancemiles": 0.0,
        "distancekilometers": 0.0,
        "cadencex2": 178,
        "elapsedtime": "00:00:00",
        "seq": 1,
        "elapsedseconds": 0.0,
    }


def expected_trackpoint_1200():
    return {
        "type": "Trackpoint",
        "time": "2014-10-05T15:15:47.000Z",
        "latitudedegrees": 44.91043584421277,
        "longitudedegrees": -93.2357053924352,
        "altitudemeters": 270.79998779296875,
        "distancemeters": 21266.9296875,
        "heartratebpm": 140,
        "speed": 2.818000078201294,
        "cadence": 86,
        "altitudefeet": 888.4514035202387,
        "distancemiles": 13.214657455149426,
        "distancekilometers": 21.2669296875,
        "cadencex2": 172,
        "elapsedtime": "02:07:54",
        "seq": 1200,
        "elapsedseconds": 7674.0,
    }


def expected_last_trackpoint():
    return {
        "type": "Trackpoint",
        "time": "2014-10-05T17:22:17.000Z",
        "latitudedegrees": 44.95180849917233,
        "longitudedegrees": -93.10493202880025,
        "altitudemeters": 263.6000061035156,
        "distancemeters": 42635.44921875,
        "heartratebpm": 161,
        "speed": 3.5460000038146977,
        "cadence": 77,
        "altitudefeet": 864.8294163501167,
        "distancemiles": 26.492439912628992,
        "distancekilometers": 42.63544921875,
        "cadencex2": 154,
        "elapsedtime": "04:14:24",
        "seq": 2256,
        "elapsedseconds": 15264.0,
    }


def expected_stats():
    return {
        "heartbeat_data": {
            "histogram": {
                "85": 2,
                "89": 2,
                "90": 2,
                "91": 3,
                "93": 1,
                "96": 2,
                "98": 1,
                "100": 1,
                "104": 1,
                "106": 1,
                "107": 1,
                "108": 3,
                "109": 2,
                "111": 1,
                "112": 1,
                "114": 4,
                "115": 2,
                "116": 1,
                "117": 7,
                "118": 2,
                "119": 3,
                "120": 3,
                "121": 5,
                "122": 3,
                "123": 4,
                "124": 8,
                "125": 15,
                "126": 5,
                "127": 17,
                "128": 22,
                "129": 12,
                "130": 17,
                "131": 23,
                "132": 37,
                "133": 39,
                "134": 34,
                "135": 49,
                "136": 70,
                "137": 82,
                "138": 113,
                "139": 223,
                "140": 221,
                "141": 195,
                "142": 192,
                "143": 124,
                "144": 81,
                "145": 72,
                "146": 75,
                "147": 61,
                "148": 77,
                "149": 55,
                "150": 47,
                "151": 39,
                "152": 32,
                "153": 29,
                "154": 21,
                "155": 12,
                "156": 16,
                "157": 17,
                "158": 8,
                "159": 5,
                "160": 12,
                "161": 8,
                "162": 5,
                "163": 7,
                "164": 3,
                "165": 3,
                "166": 1,
                "167": 4,
                "168": 3,
                "170": 7,
            },
            "total_readings": 2256,
            "highest_bpm": 170,
            "average_bpm": 141.18262411347519,
            "most_frequent_bpm": 139,
        },
        "cadence_data": {
            "histogram": {
                "88": 2,
                "92": 1,
                "94": 4,
                "100": 3,
                "102": 2,
                "104": 3,
                "106": 1,
                "108": 5,
                "110": 7,
                "112": 13,
                "114": 11,
                "116": 19,
                "118": 57,
                "120": 51,
                "122": 30,
                "124": 22,
                "126": 13,
                "128": 8,
                "130": 6,
                "132": 2,
                "134": 2,
                "136": 1,
                "138": 3,
                "140": 2,
                "142": 3,
                "144": 2,
                "146": 3,
                "148": 2,
                "152": 1,
                "154": 1,
                "156": 1,
                "158": 2,
                "160": 2,
                "162": 5,
                "164": 7,
                "166": 62,
                "168": 496,
                "170": 826,
                "172": 380,
                "174": 90,
                "176": 53,
                "178": 24,
                "180": 10,
                "182": 3,
                "184": 7,
                "186": 2,
                "188": 1,
                "234": 1,
            },
            "run_walk_separator_cadence": 150,
            "total_readings": 2252,
            "running_count": 1974,
            "walking_count": 278,
            "idle_count": 0,
            "running_pct": 87.65541740674956,
            "walking_pct": 12.344582593250445,
            "idle_pct": 0.0,
            "running_avg_cadence": 170.28571428571428,
            "walking_avg_cadence": 119.6978417266187,
        },
    }


def test_twin_cities_marathon_tcx_file():
    expected_trackpoint_count = 2256
    filename = "data/twin_cities_marathon.tcx"
    opts = dict()
    handler = ggps.TcxHandler(opts)
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

    assert handler.get_data()["stats"] == expected_stats()
