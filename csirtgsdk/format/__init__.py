from csirtgsdk.format import table, format_json, format_csv, zbro
from csirtgsdk.constants import PYVERSION

if PYVERSION == 2:
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF8')

plugins = {
    'table': table.Table,
    'csv': format_csv.CSV,
    'json': format_json.JSON,
    'bro': zbro .Bro
}


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        raise Exception("No such factory: {}".format(name))
