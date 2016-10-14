from csirtgsdk.format import table, format_json, format_csv, zbro

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
