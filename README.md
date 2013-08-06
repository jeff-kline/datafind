datafind
========

Expand, read or verify contents of a diskcache file. 

Recognized diskcache formats include single-extension and
multiple-extension.

Examples
========

Help:
```bash
$ python -m diskcache --help
Usage: diskcache.py FILE_LIST [options]

Find data using diskcache

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -m GPS_MIN, --gps-min=GPS_MIN
                        [default: None] Smallest second of interest.  Frames
                        intersecting the open interval (GPS_MIN,GPS_MIN+1) are
                        included.
  -M GPS_MAX, --gps-max=GPS_MAX
                        [default: None] Largest second of interest.  Frames
                        intersecting the open interval (GPS_MAX,GPS_MAX+1) are
                        included.
  -r REGEXP, --regexp=REGEXP
                        [default: ''] include only lines from files in
                        FILE_LIST matching regular expression.
  -c COMMAND, --command=COMMAND
                        [default: expand] valid values are verify, expand,
                        raw.
  -e, --exists          Test existence of files in diskcache. Only sensible
                        when used with '-c expand'.
  --no-update-file-count
                        If flag is present, then do not update the file_count
                        field of the diskcache.
  --no-prune            If flag is present, thenpreserve all all entries with
                        empty segmentlists.
```

List all entries in diskcache matching `trend/LHO` and which
intersect the (open) gps time interval `(1e10, 1e10+1)`:

```bash
$ python -m diskcache /ldas_outgoing/diskcacheAPI/frame_cache_dump -r trend/LHO -m 1000000000 -M 1000000000
/archive/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
/archive/frames/trend/second-trend/LHO/H-T-999/H-T-999999960-60.gwf
/data/node238/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
```

Verify that the above files listed exist on disk (pass the flag `-e`):
```bash
$ python -m diskcache /ldas_outgoing/diskcacheAPI/frame_cache_dump -r trend/LHO -m 1000000000 -M 1000000000  -e
True /archive/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
True /archive/frames/trend/second-trend/LHO/H-T-999/H-T-999999960-60.gwf
False /data/node238/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
```

Display the un-expanded diskcache information (useful for debugging):
```bash
$ python -m diskcache /ldas_outgoing/diskcacheAPI/frame_cache_dump -r trend/LHO -m 1000000000 -M 1000000000 -c raw
{'mod_time': 1315971213, 'frame_type': 'M', 'ext': '.gwf', 'file_count': 1, 'number1': 1, 'directory': '/archive/frames/trend/minute-trend/LHO/H-M-99', 'segmentlist': [segment(999997200, 1000000800)], 'dur': 3600, 'site': 'H'}
{'mod_time': 1315965229, 'frame_type': 'T', 'ext': '.gwf', 'file_count': 1, 'number1': 1, 'directory': '/archive/frames/trend/second-trend/LHO/H-T-999', 'segmentlist': [segment(999999960, 1000000020)], 'dur': 60, 'site': 'H'}
{'mod_time': 1315971491, 'frame_type': 'M', 'ext': '.gwf', 'file_count': 1, 'number1': 1, 'directory': '/data/node238/frames/trend/minute-trend/LHO/H-M-99', 'segmentlist': [segment(999997200, 1000000800)], 'dur': 3600, 'site': 'H'}
```





