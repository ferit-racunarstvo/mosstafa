def required_entries_missing(config):
    status = bool

    if not config[0] or not config[5]:
        status = True
    else:
        status = False

    return status
