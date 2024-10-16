# ggps

ggps - gps file parsing utilities for garmin connect and garmin devices


## Urls

- GitHub: https://github.com/cjoakim/ggps-py
- PyPi: https://pypi.org/project/ggps/

## Features

- Parse **gpx** and **tcx** files downloaded from Garmin Connect (https://connect.garmin.com)
- Use class **TcxHandler** to parse TCX files
  - contains the Trackpoint data with additional/augmented values, such as:
    - "elapsedtime", "elapsedseconds", "altitudefeet", "distancemiles", "distancekilometers", and "cadencex2"
  - also includes an event "stats" summary with heartbeat_data and cadence_data sections
  - the stats contains value histograms and computed values such as averages
  - cadence_data includes run/walk/idle time percentages
- Use class **GpxHandler** to parse GPX files
  - contains the Trackpoint data with additional/augmented values, such as:
    - "seq", "elapsedtime", "elapsedseconds"
- Discover the structure of the TCX/GPX/XML files with class **PathHandler**

---

## Quick start

### Installation

```
$ pip install ggps
```

### Use

#### Sample Program

See the following sample-program.py in the GitHub repo.

See the **data/** directory in the GitHub repo for the sample gpx and tcx files
processed by this sample program.

```
import json

import ggps

def parse_file(infile, handler_type):
    print("parsing file: {} type: {}".format(infile, handler_type))
    handler = None
    opts = dict()
    opts["run_walk_separator_cadence"] = 150  # 150 is the default
    # opts["no-stats"] = "any value"

    if handler_type == "tcx":
        handler = ggps.TcxHandler(opts)
    elif handler_type == "gpx":
        handler = ggps.GpxHandler(opts)
    else:
        handler = ggps.PathHandler(opts)

    handler.parse(infile)
    # print(str(handler))
    write_json_file(handler)


def write_json_file(handler, pretty=True, verbose=True) -> None:
    """Write the parsed handler data to a file in the same directory, with a .json filetype."""
    outfile = "{}.{}.json".format(handler.filename.strip(), handler.handler_type)
    jstr = None
    if pretty is True:
        jstr = json.dumps(handler.get_data(), sort_keys=False, indent=2)
    else:
        jstr = json.dumps(handler.get_data())

    with open(file=outfile, encoding="utf-8", mode="w") as file:
        file.write(jstr)
        if verbose is True:
            print(f"file written: {outfile}")


if __name__ == "__main__":

    print("ggps version {}".format(ggps.VERSION))

    # Latest files produced in 2024 with Forerunner 265S
    parse_file("data/activity_17075053124_lorimer_avinger.tcx", "tcx")
    parse_file("data/activity_17075053124_lorimer_avinger.tcx", "path")
    parse_file("data/activity_17075053124_lorimer_avinger.gpx", "gpx")
    parse_file("data/activity_17075053124_lorimer_avinger.gpx", "path")

    # Twin Cities Marathon files
    parse_file("data/twin_cities_marathon.tcx", "tcx")
    parse_file("data/twin_cities_marathon.tcx", "path")
    parse_file("data/twin_cities_marathon.gpx", "gpx")
    parse_file("data/twin_cities_marathon.gpx", "path")

    # New River 50K files
    parse_file("data/new_river_50k.tcx", "tcx")
    parse_file("data/new_river_50k.tcx", "path")
    parse_file("data/new_river_50k.gpx", "gpx")
    parse_file("data/new_river_50k.gpx", "path")

    # Davidson Track 5K files
    parse_file("data/dav_track_5k.tcx", "tcx")
    parse_file("data/dav_track_5k.tcx", "path")
    parse_file("data/dav_track_5k.gpx", "gpx")
    parse_file("data/dav_track_5k.gpx", "path")

    # activity_4564516081 files
    parse_file("data/activity_4564516081.tcx", "tcx")
    parse_file("data/activity_4564516081.tcx", "path")
    parse_file("data/activity_4564516081.gpx", "gpx")
    parse_file("data/activity_4564516081.gpx", "path")

    # activity_4564516081 files
    parse_file("data/activity_607442311.tcx", "tcx")
    parse_file("data/activity_607442311.tcx", "path")
    parse_file("data/activity_607442311.gpx", "gpx")
    parse_file("data/activity_607442311.gpx", "path")

```

#### Executing the Sample Program

```
$ python sample-program.py
```

#### Sample Program Output

```
ggps version 0.5.0
parsing file: data/activity_17075053124_lorimer_avinger.tcx type: tcx
file written: data/activity_17075053124_lorimer_avinger.tcx.tcx.json
parsing file: data/activity_17075053124_lorimer_avinger.tcx type: path
file written: data/activity_17075053124_lorimer_avinger.tcx.path.json
parsing file: data/activity_17075053124_lorimer_avinger.gpx type: gpx
file written: data/activity_17075053124_lorimer_avinger.gpx.gpx.json
parsing file: data/activity_17075053124_lorimer_avinger.gpx type: path
file written: data/activity_17075053124_lorimer_avinger.gpx.path.json
parsing file: data/twin_cities_marathon.tcx type: tcx
file written: data/twin_cities_marathon.tcx.tcx.json
parsing file: data/twin_cities_marathon.tcx type: path
file written: data/twin_cities_marathon.tcx.path.json
parsing file: data/twin_cities_marathon.gpx type: gpx
file written: data/twin_cities_marathon.gpx.gpx.json
parsing file: data/twin_cities_marathon.gpx type: path
file written: data/twin_cities_marathon.gpx.path.json
parsing file: data/new_river_50k.tcx type: tcx
file written: data/new_river_50k.tcx.tcx.json
parsing file: data/new_river_50k.tcx type: path
file written: data/new_river_50k.tcx.path.json
parsing file: data/new_river_50k.gpx type: gpx
file written: data/new_river_50k.gpx.gpx.json
parsing file: data/new_river_50k.gpx type: path
file written: data/new_river_50k.gpx.path.json
parsing file: data/dav_track_5k.tcx type: tcx
file written: data/dav_track_5k.tcx.tcx.json
parsing file: data/dav_track_5k.tcx type: path
file written: data/dav_track_5k.tcx.path.json
parsing file: data/dav_track_5k.gpx type: gpx
file written: data/dav_track_5k.gpx.gpx.json
parsing file: data/dav_track_5k.gpx type: path
file written: data/dav_track_5k.gpx.path.json
parsing file: data/activity_4564516081.tcx type: tcx
file written: data/activity_4564516081.tcx.tcx.json
parsing file: data/activity_4564516081.tcx type: path
file written: data/activity_4564516081.tcx.path.json
parsing file: data/activity_4564516081.gpx type: gpx
file written: data/activity_4564516081.gpx.gpx.json
parsing file: data/activity_4564516081.gpx type: path
file written: data/activity_4564516081.gpx.path.json
parsing file: data/activity_607442311.tcx type: tcx
file written: data/activity_607442311.tcx.tcx.json
parsing file: data/activity_607442311.tcx type: path
file written: data/activity_607442311.tcx.path.json
parsing file: data/activity_607442311.gpx type: gpx
file written: data/activity_607442311.gpx.gpx.json
parsing file: data/activity_607442311.gpx type: path
file written: data/activity_607442311.gpx.path.json
```

#### Sample Output File - TcxParser

```
{
  "filename": "data/twin_cities_marathon.tcx",
  "ggps_version": "0.5.0",
  "ggps_parsed_at": "2024-09-30 09:44:13.594348",
  "device_name": "Garmin Forerunner 620",
  "device_id": "3875991210",
  "trackpoint_count": 2256,
  "trackpoints": [
    {
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
      "elapsedseconds": 0.0
    },

    ...

    {
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
      "elapsedseconds": 15264.0
    }
  ],
  "stats": {
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
        "170": 7
      },
      "total_readings": 2256,
      "highest_bpm": 170,
      "average_bpm": 141.18262411347519,
      "most_frequent_bpm": 139
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
        "234": 1
      },
      "running_avg_cadence": 170.28571428571428,
      "walking_avg_cadence": 119.6978417266187,
      "run_walk_separator_cadence": 150,
      "total_readings": 2252,
      "running_count": 1974,
      "walking_count": 278,
      "idle_count": 0,
      "running_pct": 87.65541740674956,
      "walking_pct": 12.344582593250445,
      "idle_pct": 0.0
    }
  }
}    
```

#### Sample Output File - PathParser

```
{
  "filename": "data/twin_cities_marathon.tcx",
  "ggps_version": "0.5.0",
  "ggps_parsed_at": "2024-09-30 09:44:14.336540",
  "path_counter": {
    "TrainingCenterDatabase": 1,
    "TrainingCenterDatabase@xsi:schemaLocation": 1,
    "TrainingCenterDatabase@xmlns:ns5": 1,
    "TrainingCenterDatabase@xmlns:ns3": 1,
    "TrainingCenterDatabase@xmlns:ns2": 1,
    "TrainingCenterDatabase@xmlns": 1,
    "TrainingCenterDatabase@xmlns:xsi": 1,
    "TrainingCenterDatabase@xmlns:ns4": 1,
    "TrainingCenterDatabase|Activities": 1,
    "TrainingCenterDatabase|Activities|Activity": 1,
    "TrainingCenterDatabase|Activities|Activity@Sport": 1,
    "TrainingCenterDatabase|Activities|Activity|Id": 1,
    "TrainingCenterDatabase|Activities|Activity|Lap": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap@StartTime": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|TotalTimeSeconds": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|DistanceMeters": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|MaximumSpeed": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Calories": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|AverageHeartRateBpm": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|AverageHeartRateBpm|Value": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|MaximumHeartRateBpm": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|MaximumHeartRateBpm|Value": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Intensity": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|TriggerMethod": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Time": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position|LatitudeDegrees": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Position|LongitudeDegrees": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|AltitudeMeters": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|DistanceMeters": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|HeartRateBpm": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|HeartRateBpm|Value": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX@xmlns": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX|Speed": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Track|Trackpoint|Extensions|TPX|RunCadence": 2256,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX": 108,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX@xmlns": 108,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|MaxRunCadence": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|AvgRunCadence": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|AvgSpeed": 27,
    "TrainingCenterDatabase|Activities|Activity|Lap|Extensions|LX|Steps": 27,
    "TrainingCenterDatabase|Activities|Activity|Creator": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator@xsi:type": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Name": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|UnitId": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|ProductID": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Version": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Version|VersionMajor": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Version|VersionMinor": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Version|BuildMajor": 1,
    "TrainingCenterDatabase|Activities|Activity|Creator|Version|BuildMinor": 1,
    "TrainingCenterDatabase|Author": 1,
    "TrainingCenterDatabase|Author@xsi:type": 1,
    "TrainingCenterDatabase|Author|Name": 1,
    "TrainingCenterDatabase|Author|Build": 1,
    "TrainingCenterDatabase|Author|Build|Version": 1,
    "TrainingCenterDatabase|Author|Build|Version|VersionMajor": 1,
    "TrainingCenterDatabase|Author|Build|Version|VersionMinor": 1,
    "TrainingCenterDatabase|Author|Build|Version|BuildMajor": 1,
    "TrainingCenterDatabase|Author|Build|Version|BuildMinor": 1,
    "TrainingCenterDatabase|Author|LangID": 1,
    "TrainingCenterDatabase|Author|PartNumber": 1
  }
}
```

---

## Changelog

```
Current version: 0.5.1

-  2024/10/15, version 0.5.1   Enabled support for python 3.11
-  2024/09/30, version 0.5.0   Output as JSON files with numeric attributes
                               stats added to TCX output by default with heartbeat_data and cadence_data sections
                               configurable run_walk_separator_cadence
                               new sample program
-  2024/09/23, version 0.4.1,  Fix pyproject.toml project description
-  2024/09/23, version 0.4.0,  Upgraded to python 3.12, pyproject.toml build mechanism, latest m26 >=0.3.1
-  2020/02/22, version 0.3.0,  Parsing improvements, normalize 'cadence' and 'heartratebpm' attribute names
-  2020/02/19, version 0.2.1,  Upgraded the m26 and Jinga2 libraries
-  2017/09/27, version 0.2.0,  Converted to the pytest testing framework
-  2017/09/26, version 0.1.13, packagin.
-  2016/11/07, version 0.1.12, updated packaging
-  2016/11/07, version 0.1.11, updated packaging
-  2016/11/07, version 0.1.10, updated packaging
-  2016/11/07, version 0.1.9,  updated packaging
-  2016/11/07, version 0.1.8,  updated packaging
-  2016/11/06, version 0.1.7,  updated description
-  2016/11/06, version 0.1.6,  republished
-  2016/11/06, version 0.1.5,  refactored ggps/ dir
-  2016/11/06, version 0.1.4,  refactored ggps/ dir. nose2 for tests
-  2015/11/07, version 0.1.3,  Added README.rst
-  2015/11/07, version 0.1.1   Initial release
```