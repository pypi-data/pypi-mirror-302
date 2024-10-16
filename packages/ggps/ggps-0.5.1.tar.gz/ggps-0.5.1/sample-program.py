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
