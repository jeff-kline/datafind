datafind
========

Expand, read or verify contents of a diskcache file. 

Recognized diskcache formats include single-extension and
multiple-extension.

Examples
========

List all entries in diskcache matching `/archive/.*/LHO` and which
contain the gps second `[1e10, 1e10 + 1]`:

```bash
$ python -m diskcache /ldas_outgoing/diskcacheAPI/frame_cache_dump -r '/archive/.*/LHO' -m 1000000000 -M 1000000000 -e
/archive/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
/archive/frames/trend/second-trend/LHO/H-T-999/H-T-999999960-60.gwf
```



