import json
import xml.sax

from ggps.base_handler import BaseHandler


class PathHandler(BaseHandler):

    def parse(self, filename):
        self.filename = filename
        self.handler_type = "path"
        xml.sax.parse(open(filename), self)
        return self

    def __init__(self, opts: dict = {}):
        BaseHandler.__init__(self, opts)

    def startElement(self, name, attrs):
        self.heirarchy.append(name)
        path = self.curr_path()
        self.path_counter[path] += 1

        for aname in attrs.getNames():
            self.path_counter[path + "@" + aname] += 1

    def endElement(self, name):
        self.heirarchy.pop()

    def curr_path(self):
        return "|".join(self.heirarchy)

    # def __str__(self):
    #     return json.dumps(self.path_counter, sort_keys=True, indent=2)
