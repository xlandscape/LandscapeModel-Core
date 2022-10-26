import datetime

def convert_index(index, source_scale, target_scale):
    if source_scale == target_scale:
        target_index = index
    elif target_scale == "global":
        target_index = index
    elif source_scale == "time/day" and target_scale == "time/year":
        target_index = datetime.datetime.fromordinal(index).year
    else:
        raise NotImplementedError("Conversion from {source_scale} to {target_scale} not implemented!")
    return target_index
