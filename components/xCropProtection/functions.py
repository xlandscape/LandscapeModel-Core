import typing
import datetime

def convert_index(index: typing.Tuple[int], source_scale: str, target_scale: str) -> typing.Tuple[int]:
    if source_scale == target_scale:
        target_index = index
    elif target_scale == "global":
        target_index = (0,)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "time/day":
        target_index = (index[0],)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "time/year":
        target_index = (datetime.datetime.fromordinal(index[0]).year,)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "time/simulation":
        target_index = (0,)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "space/base_geometry":
        target_index = (index[1],)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "time/year, space/base_geometry":
        target_index = (datetime.datetime.fromordinal(index[0]).year, index[1])
    elif source_scale == "time/day, space/base_geometry" and target_scale == "time/simulation, space/base_geometry":
        target_index = (0, index[1])
    elif source_scale == "time/day, space/base_geometry" and target_scale == "other/products":
        target_index = (0,)
    elif source_scale == "time/day, space/base_geometry" and target_scale == "other/active_substances":
        target_index = (0,)
    elif source_scale == "time/day, space/base_geometry" and target_scale == None:
        target_index = (0,)
    else:
        raise NotImplementedError(f"Conversion from {source_scale} to {target_scale} not implemented!")
    return target_index
