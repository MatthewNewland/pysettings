from pysettings import Backend, CONFIGDIR
import json
import os


class JSONBackend(Backend):

    def __init__(self):
        self.filename = os.path.join(CONFIGDIR, self.org_name, self.app_name)
        self.filename += ".conf.json"

    def read(self):
        with open(self.filename) as fh:
            self.store = json.load(fh)

    def write(self):
        with open(self.filename, 'w') as fh:
            json.dump(self.store, fh)

