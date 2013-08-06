datafind
========

Expand, read or verify contents of a diskcache file. 

Recognized diskcache formats are single-extension `(0x00ff)` and
multiple-extension `(0x0101)`. 

Examples
========

```bash
$ python -m diskcache /ldas_outgoing/diskcacheAPI/frame_cache_dump -r '/archive/.*/LHO' -m 1000000000 -M 1000000000 -e
True /archive/frames/trend/minute-trend/LHO/H-M-99/H-M-999997200-3600.gwf
True /archive/frames/trend/second-trend/LHO/H-T-999/H-T-999999960-60.gwf
```



