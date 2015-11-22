"""
Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import itertools
import re


def make_ranges(ranges_string, upper):
    """
    Make ranges from the specified string.
    """
    ranges = itertools.chain(
        *itertools.starmap(
            range,
            (
                parse_range(i, upper)
                for i in ranges_string.split('+') if check_range(i)
            )
        )
    )

    return ranges


def parse_range(range_string, upper):
    """
    Parse a range.
    """
    # four cases of range_string: '' '7-' '-9' '10'
    # one more case: '1-8'

    if range_string == '':
        return 1, upper

    if range_string.endswith('-'):
        range_string += '0'
    if range_string.startswith('-'):
        range_string = '1' + range_string

    single_range = range_string.split('-')
    start = int(single_range[0])
    end = int(single_range[1]) if len(single_range) == 2 else start

    end = end if end and end <= upper else upper
    start = start if start and start <= end else 0
    return start, end + 1


def check_range(range_string):
    """
    Validate the range.
    """
    if range_string == '':
        return True
    # awkward ad-hoc emulation of re.fullmatch
    if re.sub(
            r'\d+\-\d+|\d+\-|\-\d+|\d+', '', range_string, 1
    ) == '':
        return True
    return False
