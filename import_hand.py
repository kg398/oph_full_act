import re
import numpy as np
from operator import mul
from functools import reduce

def read_and_strip(filename):
    with open(filename, 'r') as f:
        content = f.read()
    # Remove spaces and tabs (mimics erase(...,' ') and erase(...,char(9)))
    return content.replace(' ', '').replace('\t', '')


def find_delims(s):
    return [i for i, c in enumerate(s) if c == ';']


def end_index(start_i, delims):
    """Return the position of the next semicolon after start_i."""
    for d in delims:
        if d > start_i:
            return d
    return len(s)


def extract_value(s, key, offset, delims):
    """Extract a numeric array from s after key+offset chars, up to next ';'."""
    start_i = s.find(key)
    if start_i == -1:
        return None
    end = end_index(start_i, delims)
    return list(map(float, s[start_i + offset: end].replace('[','').replace(']','').split(',')))


def load_hand_config(filename):
    s = read_and_strip(filename)
    delims = find_delims(s)

    h = {}

    # --- Scalars ---
    h['li'] = extract_value(s, 'lig_index', 10, delims)
    h['pi'] = extract_value(s, 'p_index',    8, delims)
    h['pt'] = extract_value(s, 'p_thumb',    8, delims)
    h['ap'] = extract_value(s, 'a_print',    8, delims)

    # --- Per-finger data: index=0, middle=1, ring=2, little=3, thumb=4 ---
    fingers = [
        ('index',  '_index',  9, 9, 8, 8, 8),   # bl+9, jd+9, o+8, a+8, w+8
        ('middle', '_middle', 10,10, 9, 9, 9),
        ('ring',   '_ring',    8, 8, 7, 7, 7),
        ('little', '_little', 10,10, 9, 9, 9),
        ('thumb',  '_thumb',   9, 9, 8, 8, 8),
    ]

    rows = len(fingers)
    h['bl'] = [None] * rows
    h['jd'] = [None] * rows
    h['o']  = [None] * rows
    h['a']  = [None] * rows
    h['w']  = [None] * rows

    for row, (name, suffix, bl_off, jd_off, o_off, a_off, w_off) in enumerate(fingers):

        # bl
        h['bl'][row] = extract_value(s, 'bl' + suffix, bl_off, delims)

        # jd (with optional base_jd_<finger> substitution)
        base_jd_key = 'base_jd' + suffix
        base_jd_i = s.find(base_jd_key)
        if base_jd_i == -1:
            h['jd'][row] = extract_value(s, 'jd' + suffix, jd_off, delims)
        else:
            base_joint = s[base_jd_i + len(base_jd_key) + 1:
                           end_index(base_jd_i, delims)]
            # find second occurrence of jd<suffix>
            first = s.find('jd' + suffix)
            second = s.find('jd' + suffix, first + 1)
            end = end_index(second, delims)
            raw = s[second + jd_off: end].replace(base_jd_key, base_joint).replace('[','').replace(']','').split(',')
            for i in range(0,len(raw)):
                raw[i] = reduce(mul, list(map(float,raw[i].split('*'))), 1)
            h['jd'][row] = raw

        # o
        h['o'][row] = extract_value(s, 'o' + suffix, o_off, delims)

        # a
        h['a'][row] = extract_value(s, 'a' + suffix, a_off, delims)

        # w (with optional base_w_<finger> substitution)
        base_w_key = 'base_w' + suffix
        base_w_i = s.find(base_w_key)
        if base_w_i == -1:
            h['w'][row] = extract_value(s, 'w' + suffix, w_off, delims)
        else:
            base_w = s[base_w_i + len(base_w_key) + 1:
                       end_index(base_w_i, delims)]
            first = s.find('w' + suffix)
            second = s.find('w' + suffix, first + 1)
            end = end_index(second, delims)
            raw = s[second + w_off: end].replace(base_w_key, base_w).replace('[','').replace(']','').split(',')
            for i in range(0,len(raw)):
                raw[i] = reduce(mul, list(map(float,raw[i].split('*'))), 1)
            h['w'][row] = raw

    return h