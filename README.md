datafind
========

Expand, read or verify contents of a diskcache file. 

Recognized diskcache formats include single-extension and
multiple-extension.

Examples
========

List all entries in diskcache matching `trend/LHO` and which
contain the gps second `[1e10, 1e10 + 1]`:

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





