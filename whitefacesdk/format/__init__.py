from whitefacesdk.format.table import Table

plugins = {
    'table': Table,
}


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        return None
