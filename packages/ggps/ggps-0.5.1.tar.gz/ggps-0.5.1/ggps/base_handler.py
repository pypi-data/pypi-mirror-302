import json
import xml.sax

from collections import defaultdict
from datetime import datetime

import m26

from ggps.counter import Counter
from ggps.trackpoint import Trackpoint
from ggps import VERSION
from ggps import DEFAULT_RUN_WALK_SEPARATOR_CADENCE


class BaseHandler(xml.sax.ContentHandler):

    def __init__(self, opts: dict = {}):
        xml.sax.ContentHandler.__init__(self)
        self.opts = opts
        self.filename = None
        self.handler_type = None
        self.heirarchy = list()
        self.trackpoints = list()
        self.curr_tkpt = Trackpoint()
        self.curr_text = ""
        self.end_reached = False
        self.first_time = None
        self.first_etime = None
        self.first_time_secs_to_midnight = 0
        self.path_counter = defaultdict(int)
        self.version = VERSION
        self.device_name = None
        self.device_id = None
        self.run_walk_separator_cadence = DEFAULT_RUN_WALK_SEPARATOR_CADENCE

        if "run_walk_separator_cadence" in opts.keys():
            try:
                self.run_walk_separator_cadence = int(
                    opts["run_walk_separator_cadence"]
                )
            except:
                self.run_walk_separator_cadence = 150

    def __str__(self):
        return json.dumps(self.get_data(), sort_keys=False, indent=2)

    def get_data(self) -> dict:
        """Return a JSON serializable dictionary of the data in this handler."""
        data = dict()
        data["filename"] = self.filename
        data["ggps_version"] = self.version
        data["ggps_parsed_at"] = str(datetime.now())

        if self.handler_type == "path":
            data["path_counter"] = self.path_counter
        else:
            cadence_counter = Counter()
            heartbeat_counter = Counter()
            if self.handler_type == "tcx":
                data["device_name"] = self.device_name
                data["device_id"] = self.device_id
            data["trackpoint_count"] = self.trackpoint_count()
            data["trackpoints"] = list()
            for idx, t in enumerate(self.trackpoints):
                t.set("seq", str(idx + 1))
                t.post_parse()
                data["trackpoints"].append(t.values)
                if self.handler_type == "tcx":
                    if "cadencex2" in t.values.keys():
                        cadence_counter.increment(t.get("cadencex2"))
                    if "heartratebpm" in t.values.keys():
                        heartbeat_counter.increment(t.get("heartratebpm"))

            if self.handler_type == "tcx":
                if "no-stats" in self.opts.keys():
                    pass
                else:
                    # construct the stats nested dictionary
                    stats, heartbeat_data, cadence_data = dict(), dict(), dict()
                    stats["heartbeat_data"] = heartbeat_data
                    stats["cadence_data"] = cadence_data
                    data["stats"] = stats

                    # populate heartbeat_data
                    cdata = heartbeat_counter.get_data()
                    heartbeat_data["histogram"] = cdata
                    total_count = 0
                    total_heartbeats = 0
                    total_heartbeat_readings = 0
                    highest_bpm = 0
                    for key in heartbeat_counter.get_data().keys():
                        bpm = int(key)
                        cnt = cdata[key]
                        total_heartbeat_readings = total_heartbeat_readings + cnt
                        total_heartbeats = total_heartbeats + (bpm * cnt)
                        if bpm > highest_bpm:
                            highest_bpm = bpm
                    heartbeat_data["total_readings"] = total_heartbeat_readings
                    heartbeat_data["highest_bpm"] = highest_bpm
                    if total_heartbeat_readings > 0:
                        heartbeat_data["average_bpm"] = float(total_heartbeats) / float(
                            total_heartbeat_readings
                        )
                    heartbeat_data["most_frequent_bpm"] = (
                        heartbeat_counter.most_frequent()
                    )

                    # populate cadence_data
                    cdata = cadence_counter.get_data()
                    cadence_data["histogram"] = cdata
                    cadence_data["running_avg_cadence"] = 0.0  # default
                    cadence_data["walking_avg_cadence"] = 0.0  # default

                    running_count = 0
                    walking_count = 0
                    idle_count = 0
                    running_steps = 0
                    walking_steps = 0
                    for key in cadence_counter.get_data().keys():
                        cad = int(key)
                        cnt = cdata[key]
                        if cad == 0:
                            idle_count = idle_count + cnt
                        else:
                            if cad >= self.run_walk_separator_cadence:
                                running_count = running_count + cnt
                                running_steps = running_steps + (cad * cnt)
                            else:
                                walking_count = walking_count + cnt
                                walking_steps = walking_steps + (cad * cnt)

                    total_count = running_count + walking_count + idle_count
                    cadence_data["run_walk_separator_cadence"] = (
                        self.run_walk_separator_cadence
                    )
                    cadence_data["total_readings"] = total_count
                    cadence_data["running_count"] = running_count
                    cadence_data["walking_count"] = walking_count
                    cadence_data["idle_count"] = idle_count

                    cadence_data["running_pct"] = (
                        float(running_count) / float(total_count) * 100.0
                    )
                    cadence_data["walking_pct"] = (
                        float(walking_count) / float(total_count) * 100.0
                    )
                    cadence_data["idle_pct"] = (
                        float(idle_count) / float(total_count) * 100.0
                    )

                    # cadence_data["running_steps"] = running_steps
                    # cadence_data["walking_steps"] = walking_steps
                    # cadence_data["total_steps"] = running_steps + walking_steps

                    if running_count > 0:
                        cadence_data["running_avg_cadence"] = float(
                            running_steps
                        ) / float(running_count)

                    if walking_count > 0:
                        cadence_data["walking_avg_cadence"] = float(
                            walking_steps
                        ) / float(walking_count)

        return data

    def endDocument(self):
        self.completed = True

    def characters(self, chars):
        if self.curr_text:
            self.curr_text = self.curr_text + chars
        else:
            self.curr_text = chars

    def reset_curr_text(self):
        self.curr_text = ""

    def curr_depth(self):
        return len(self.heirarchy)

    def curr_path(self):
        return "|".join(self.heirarchy)

    def trackpoint_count(self):
        return len(self.trackpoints)

    def set_first_trackpoint(self, t):
        self.first_time = t.get("time")
        self.first_hhmmss = self.parse_hhmmss(self.first_time)
        self.first_etime = m26.ElapsedTime(self.first_hhmmss)
        self.first_time_secs = self.first_etime.secs

        # deal with the possibility that the Activity spans two calendar days.
        secs = int(m26.Constants.seconds_per_hour() * 24)
        self.first_time_secs_to_midnight = secs - self.first_time_secs

    def meters_to_feet(self, t, meters_key, new_key):
        m = t.get(meters_key)
        km = float(m) / 1000.0
        d_km = m26.Distance(km, m26.Constants.uom_kilometers())
        yds = d_km.as_yards()
        t.set(new_key, str(yds * 3.000000))

    def meters_to_km(self, t, meters_key, new_key):
        m = t.get(meters_key)
        km = float(m) / 1000.0
        t.set(new_key, str(km))

    def meters_to_miles(self, t, meters_key, new_key):
        m = t.get(meters_key)
        km = float(m) / 1000.0
        d_km = m26.Distance(km, m26.Constants.uom_kilometers())
        t.set(new_key, str(d_km.as_miles()))

    def cadence_x2(self, t):
        c = t.get("cadence", 0)
        i = int(c)
        if i > 0:
            t.set("cadencex2", str(i * 2))

    def calculate_elapsed_time(self, t):
        time_str = t.get("time")
        new_key = "elapsedtime"
        if time_str:
            if time_str == self.first_time:
                t.set(new_key, "00:00:00")
            else:
                curr_time = self.parse_hhmmss(time_str)
                curr_etime = m26.ElapsedTime(curr_time.strip())
                secs_diff = curr_etime.secs - self.first_time_secs
                if secs_diff < 0:
                    secs_diff = secs_diff + self.first_time_secs_to_midnight
                elapsed = m26.ElapsedTime(secs_diff)
                t.set(new_key, elapsed.as_hhmmss())

    def parse_hhmmss(self, time_str):
        """
        For a given datetime value like '2014-10-05T17:22:17.000Z' return the
        hhmmss value '17:22:17'.
        """
        if len(time_str) > 0:
            if "T" in time_str:
                return str(time_str.split("T")[1][:8])
            else:
                return ""
        else:
            return ""
