import math
import statistics


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    s = round(size_bytes / power, 2)
    return "%s %s" % (s, size_name[i])


def get_median(file_sizes):
    return statistics.median(file_sizes)