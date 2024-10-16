import json

from m26 import ElapsedTime

"""
This is a datastructure class to hold the parsed contents of a 
GPX <trkpt> or TCX <Trackpoint> element.  All attribute types
are strings during the XML parsing process.  But the post_parse()
method transforms the string values into the appropriate datatypes -
such as int, float, or str.
"""


class Trackpoint(object):

    def __init__(self):
        self.values = dict()
        self.values["type"] = "Trackpoint"

    def get(self, key, default_value=""):
        if key in self.values:
            return self.values[key]
        else:
            return default_value

    def set(self, key, value):
        if key and value:
            if ":" in key:
                ns_removed_tagname = key.split(":")[1]
                self.values[ns_removed_tagname.lower().strip()] = value.strip()
            else:
                self.values[key.lower().strip()] = value.strip()

    def __str__(self):
        template = "<Trackpoint values count:{0}>"
        return template.format(len(self.values))

    def __repr__(self):
        return json.dumps(self.values, sort_keys=True, indent=2)

    def post_parse(self):
        """Convert the XML-parsed strings into the appropriate datatypes."""
        self.to_int("seq")
        if "cadence" in self.values.keys():
            self.to_int("cadence")
            self.to_int("cadencex2")
        self.to_int("heartratebpm")
        self.to_float("latitudedegrees")
        self.to_float("longitudedegrees")
        self.to_float("altitudemeters")
        self.to_float("altitudefeet")
        self.to_float("distancemeters")
        self.to_float("distancemiles")
        self.to_float("distancekilometers")
        self.to_float("speed")
        self.calculate_elapsedseconds()

    def to_int(self, key):
        try:
            if key in self.values.keys():
                self.values[key] = int(self.values[key])
        except:
            self.values[key] = 0
            print(
                "ggps.Trackpoint - error converting {} {} to int".format(
                    key, self.values[key]
                )
            )

    def to_float(self, key):
        try:
            if key in self.values.keys():
                self.values[key] = float(self.values[key])
        except:
            self.values[key] = 0.0
            print(
                "ggps.Trackpoint - error converting {} {} to float".format(
                    key, self.values[key]
                )
            )

    def calculate_elapsedseconds(self):
        if "elapsedtime" in self.values.keys():
            et = ElapsedTime(self.values["elapsedtime"])
            self.values["elapsedseconds"] = et.secs
