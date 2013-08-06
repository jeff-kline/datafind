#!/usr/bin/python
from diskcache import *
from tempfile import NamedTemporaryFile
from time import sleep
from re import compile
from glue.segments import *

import unittest

# single frame type (default is .gwf)
# DIR,SITE,FT,1,DUR TS COUNT {SL}
content_0x00ff = """/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}
/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,1,3600 1193314065 10 {876128400 876142800 876164400 876168000 876182400 876200400}
/data/node1/frames/VSR3/HrecOnline/Virgo/V-HrecOnline-9646,V,HrecOnline,1,4000 1280692798 25 {964600000 964700000}
/data/node1/frames/trend/minute-trend/LLO/L-M-60,L,M,1,3600 1110931999 840 {606944859 607049259 607051747 607476547 607479179 607558379 607564071 607625271 607626595 609185395 609200298 609513498 609519475 610001875}
/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,H,H2_RDS_C03_L2,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}
/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,1,3600 1110931999 840 {606944859 1606944859}"""

# new version
# DIR,SITE,FT,EXT,1,DUR TS COUNT {SL}
# magic string
content_0x0101 = """# version: 0x0101
/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,.gwf,1,3504 1193314065 1 {876168000 876171504}
/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,.gwf,1,3600 1193314065 10 {876128400 876142800 876164400 876168000 876182400 876200400}
/data/node1/frames/VSR3/HrecOnline/Virgo/V-HrecOnline-9646,V,HrecOnline,.gwf,1,4000 1280692798 25 {964600000 964700000}
/data/node1/frames/trend/minute-trend/LLO/L-M-60,L,M,.gwf,1,3600 1110931999 840 {606944859 607049259 607051747 607476547 607479179 607558379 607564071 607625271 607626595 609185395 609200298 609513498 609519475 610001875}
/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,H,H2_RDS_C03_L2,.gwf,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}
/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.gwf,1,3600 1110931999 840 {606944859 609968859}
/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.xml,1,3600 1110931999 840 {606944859 609968859}"""

NUMV = 3
NUMH = 1
NUML = 1

NUM_GWF = 6
NUM_XML = 1

class TestDiskcache(unittest.TestCase):
    def setUp(self):
        self._file_0x00ff = NamedTemporaryFile()
        self._file_0x00ff.write(content_0x00ff)
        self._file_0x00ff.flush()

        self._file_0x0101 = NamedTemporaryFile()
        self._file_0x0101.write(content_0x0101)
        self._file_0x0101.flush()
        self.fname_0x00ff = self._file_0x00ff.name
        self.fname_0x0101 = self._file_0x0101.name

        self.file_l = [self._file_0x00ff, self._file_0x0101]

        self.dc_keys = ['directory', 'site', 'frame_type', 'ext',
                        'number1', 'dur', 'mod_time',
                        'file_count', 'segmentlist']

    def tearDown(self):
        for f in self.file_l:
            f.close()

    def testdc_min_gps(self):
        min_gps = 867646288
        dc = DiskCacheFile(self.fname_0x00ff, minimum_gps=867646288)
        for d in dc:
            for s in d["segmentlist"].shift(d["dur"]):
                self.assertTrue(min_gps <= s[0])

    def testdc_max_gps(self):
        max_gps = 867646288
        dc = DiskCacheFile(self.fname_0x00ff, maximum_gps=867646288)
        for d in dc:
            for s in d["segmentlist"]:
                self.assertTrue( max_gps + d["dur"] >= s[1])


    def testdc_min_max_gps(self):
        min_gps = 867646288
        max_gps = 867646288
        dc = DiskCacheFile(self.fname_0x00ff, minimum_gps=867646288, maximum_gps=867646288)
        for d in dc:
            for s in d["segmentlist"]:
                self.assertEquals(s[1] - s[0], d["dur"])
            if d["segmentlist"]:
                self.assertEquals(len(d["segmentlist"]), 1)

    def testdc_version_test_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(dc.version, 0x00ff)

    def testdc_version_test_extension_0x00ff_not_set(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(dc.extension, ".gwf")
    def testdc_version_test_extension_0x00ff_is_set(self):
        dc = DiskCacheFile(self.fname_0x00ff, extension=".blah")
        self.assertEquals(dc.extension, ".blah")
        
    def testdc_version_test_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        self.assertEquals(dc.version, 0x0101)

    def testdc_version_test_extension_0x0101(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertTrue(dc.extension, None)

    def testdc_init_no_filter_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(len(dc), len(content_0x00ff.split('\n')))
        for d in dc:
            for k in self.dc_keys:
                self.assertTrue(k in d)

    def testdc_init_no_filter_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        # ignore the newline at the top of content_0x0101
        self.assertEquals(len(dc), len(content_0x0101.split('\n'))-1)
        for d in dc:
            for k in self.dc_keys:
                self.assertTrue(k in d)

    def testdc_init_empty_0x00ff(self):
        filter_list = [lambda x: False]

        dc = DiskCacheFile(self.fname_0x00ff, filter_list=filter_list)
        self.assertEquals(dc, [])

    def testdc_init_empty_0x0101(self):
        filter_list = [lambda x: False]

        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(dc, [])

    def testdc_init_full_0x00ff(self):
        filter_list = [lambda x: True]
        dc0 = DiskCacheFile(self.fname_0x00ff, filter_list=filter_list)
        dc1 = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(dc0, dc1)

    def testdc_init_full_0x0101(self):
        filter_list = [lambda x: True]
        dc0 = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        dc1 = DiskCacheFile(self.fname_0x0101)
        self.assertEquals(dc0, dc1)

    def testdc_init_with_filter_0x00ff(self):
        filter_list = [lambda x: x['site'] == 'H',]
        dc = DiskCacheFile(self.fname_0x00ff, filter_list=filter_list)
        self.assertEquals(len(dc), NUMH)

        filter_list = [lambda x: x['site'] == 'V',]
        dc = DiskCacheFile(self.fname_0x00ff, filter_list=filter_list)
        self.assertEquals(len(dc), NUMV)

        filter_list = [lambda x: x['site'] == 'L',]
        dc = DiskCacheFile(self.fname_0x00ff, filter_list=filter_list)
        self.assertEquals(len(dc), NUML)

    def testdc_init_with_filter_0x0101(self):
        filter_list = [lambda x: x['site'] == 'H',]
        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(len(dc), NUMH)

        filter_list = [lambda x: x['site'] == 'V',]
        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(len(dc), NUMV)

        filter_list = [lambda x: x['site'] == 'L',]
        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(len(dc), NUML)

        filter_list = [lambda x: x['ext'] == '.gwf',]
        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(len(dc), NUM_GWF)

        filter_list = [lambda x: x['ext'] == '.xml',]
        dc = DiskCacheFile(self.fname_0x0101, filter_list=filter_list)
        self.assertEquals(len(dc), NUM_XML)

    def testdc_init_with_regexp_0x00ff(self):
        regexp = '.*L-M-600,K,M,1,3600.*'
        dc = DiskCacheFile(self.fname_0x00ff, regexp = regexp)
        self.assertEquals(len(dc), 1)

        dc = DiskCacheFile(self.fname_0x00ff, regexp = compile(regexp))
        self.assertEquals(len(dc), 1)

    def testdc_init_with_regexp_0x0101(self):
        regexp = '.*L-M-600,K,M.*'
        dc = DiskCacheFile(self.fname_0x0101, regexp = regexp)
        self.assertEquals(len(dc), 2)

        dc = DiskCacheFile(self.fname_0x0101, regexp = compile(regexp))
        self.assertEquals(len(dc), 2)


    def testdc_init_with_pair_filters(self):
        for f in [self.fname_0x00ff, self.fname_0x0101]:
            filter_list = [lambda x: x['site'] == 'H',
                           lambda x: x['frame_type'] == 'HrecOnline']
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)

            filter_list = [lambda x: x['site'] == 'V',
                           lambda x: x['frame_type'] == 'HrecOnline']

            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), NUMV)

            filter_list = [lambda x: x['site'] == 'L',
                           lambda x: x['frame_type'] == 'HrecOnline']

            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)

    def testdc_init_with_three_filters(self):
        for f in [self.fname_0x00ff, self.fname_0x0101]:
            filter_list = [lambda x: x['site'] == 'H',
                           lambda x: x['frame_type'] == 'H2_RDS_C03_L2',
                           lambda x: '/data/' in x['directory']]
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), NUMH)

            filter_list = [lambda x: x['site'] == 'V',
                           lambda x: x['frame_type'] == 'HrecOnline',
                           lambda x: '/data/' in x['directory']]

            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), NUMV)
            
            filter_list = [lambda x: x['site'] == 'L',
                           lambda x: x['frame_type'] == 'M',
                           lambda x: '/data/node1' in x['directory']]

            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), NUML)


            filter_list = [lambda x: x['site'] == 'H',
                           lambda x: x['frame_type'] == 'H2_RDS_C03_L2',
                           lambda x: '/data/z' in x['directory']]
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)

            filter_list = [lambda x: x['site'] == 'V',
                           lambda x: x['frame_type'] == 'HrecOnline',
                           lambda x: '/data/z' in x['directory']]
            
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)
            
            filter_list = [lambda x: x['site'] == 'L',
                           lambda x: x['frame_type'] == 'M',
                           lambda x: '/data/z' in x['directory']]

            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)

    def testdc_init_with_four_filters(self):
        for f in [self.fname_0x00ff, self.fname_0x0101]:
            filter_list = [lambda x: x['site'] == 'H',
                           lambda x: x['frame_type'] == 'H2_RDS_C03_L2',
                           lambda x: '/data/' in x['directory'],
                           lambda x: x['segmentlist'].intersects_segment(
                               segment(867606096, 867606111))
            ]
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), NUMH)

            filter_list = [lambda x: x['site'] == 'H',
                           lambda x: x['frame_type'] == 'H2_RDS_C03_L2',
                           lambda x: '/data/' in x['directory'],
                           lambda x: x['segmentlist'].intersects_segment(segment(0, 1))
                       ]
            dc = DiskCacheFile(f, filter_list=filter_list)
            self.assertEquals(len(dc), 0)

    def testinvalid_content_0x00ff(self):
        tmp_c = '\n'.join([content_0x00ff,"""/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,H,H2_RDS_C03_L2,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}"""])
        with NamedTemporaryFile() as fh:
            fh.write(tmp_c)
            fh.flush()
            self.assertRaisesRegexp(ValueError, "Nonunique key in diskcache", 
                                        DiskCacheFile, fh.name)


    def testinvalid_content_0x0101(self):
        tmp_c = '\n'.join([content_0x0101,"""/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,H,H2_RDS_C03_L2,.gwf,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}"""])
        with NamedTemporaryFile() as fh:
            fh.write(tmp_c)
            fh.flush()
            self.assertRaisesRegexp(ValueError, "Nonunique key in diskcache", 
                                        DiskCacheFile, fh.name)

    def testOK_content_0x00ff(self):
        tmp_c = '\n'.join([content_0x00ff,"""/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,L,H2_RDS_C03_L2,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}"""])
        with NamedTemporaryFile() as fh:
            fh.write(tmp_c)
            fh.flush()
            dc = DiskCacheFile(fh.name)
            self.assertEquals(len(dc), NUMH + NUMV + NUML + 1 + 1)

    def testOK_content_0x0101(self):
        tmp_c = '\n'.join([content_0x0101,"""/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,L,H2_RDS_C03_L2,.gwf,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}"""])
        with NamedTemporaryFile() as fh:
            fh.write(tmp_c)
            fh.flush()
            dc = DiskCacheFile(fh.name)
            # plus 1 xml line!
            self.assertEquals(len(dc), NUMH + NUMV + NUML + 1 + 1 + 1)

        tmp_c = '\n'.join([content_0x0101,"""/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,L,H2_RDS_C03_L2,.xml,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}"""])
        with NamedTemporaryFile() as fh:
            fh.write(tmp_c)
            fh.flush()
            dc = DiskCacheFile(fh.name)
            # plus 1 xml line!
            self.assertEquals(len(dc), NUMH + NUMV + NUML + 1 + 1 + 1)

    def testsegmentlist_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(abs( dc.segmentlist()[0]), 1e9)
        self.assertEquals(len( dc.segmentlist()), 1)

    def testsegmentlist_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        self.assertEquals(abs( dc.segmentlist()[0]), 3057016)
        self.assertEquals(len( dc.segmentlist()), 23)

    def test__contains__0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        # /data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,1,3600 1193314065 10 {876128400 876142800 876164400 876168000 876182400 876200400}
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3600.gwf'
        self.assertTrue(p in dc)

        # nonsense
        for p in ['zzz', 1, [], {}]:
            self.assertFalse(p in dc)

        # dur
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3601.gwf'
        self.assertFalse(p in dc)

        # gps
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128401-3600.gwf'
        self.assertTrue(p in dc)
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128399-3600.gwf'
        self.assertFalse(p in dc)

        # frame_type
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-zHrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # site
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/z-HrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # directory
        p = '/data/node1z/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # extension
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128401-3600.sft'
        self.assertFalse(p in dc)
        dc.extension = '.sft'
        self.assertTrue(p in dc)

    def test_fail_set_extension_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        def f(): dc.extension = "foo"
        self.assertRaisesRegexp(ValueError,  "Cannot set extension with the current version", f)

    def test__contains__0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        # /data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,1,3600 1193314065 10 {876128400 876142800 876164400 876168000 876182400 876200400}
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3600.gwf'
        self.assertTrue(p in dc)

        # nonsense
        for p in ['zzz', 1, [], {}]:
            self.assertFalse(p in dc)

        # dur
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3601.gwf'
        self.assertFalse(p in dc)

        # gps
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128401-3600.gwf'
        self.assertTrue(p in dc)
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128399-3600.gwf'
        self.assertFalse(p in dc)

        # frame_type
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-zHrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # site
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/z-HrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # directory
        p = '/data/node1z/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128400-3600.gwf'
        self.assertFalse(p in dc)

        # extension
        p = '/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761/V-HrecOnline-876128401-3600.sft'
        self.assertFalse(p in dc)

        # xml extension
        # "/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.gwf,1,3600 1110931999 840 {606944859 1606944859}"""
        # "/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.xml,1,3600 1110931999 840 {606944859 1606944859}"""
        p = "/data/node1/frames/trend/minute-trend/LLO/L-M-600/K-M-606944859-3600.xml"
        self.assertTrue(p in dc)
        p = "/data/node1/frames/trend/minute-trend/LLO/L-M-600/K-M-606944859-3600.xmlz"
        self.assertFalse(p in dc)
        p = "/data/node1/frames/trend/minute-trend/LLO/L-M-600/K-M-606944859-3600.gwf"
        self.assertTrue(p in dc)

    def testkeys_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        self.assertEquals(
            set(['mod_time', 'segmentlist', 'frame_type', 'site', 
                 'file_count', 'directory', 'dur', 'number1', 'ext']),
            set(dc.dict_keys()))

    def testkeys_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        self.assertEquals(
            set(['mod_time', 'segmentlist', 'frame_type', 'site', 
                 'file_count', 'directory', 'dur', 'number1', 'ext']),
            set(dc.dict_keys()))

    def testDiskCacheFile_refresh_fail_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        sleep(1)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}'
        self._file_0x00ff.write(tmp_content)
        self._file_0x00ff.flush()
        sleep(1)
        self.assertRaisesRegexp(ValueError, "Nonunique key in diskcache", dc.refresh)

    def testDiskCacheFile_refresh_fail_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        sleep(1)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,.gwf,1,3504 1193314065 1 {876168000 876171504}'
        self._file_0x0101.write(tmp_content)
        self._file_0x0101.flush()
        sleep(1)
        self.assertRaisesRegexp(ValueError, "Nonunique key in diskcache", dc.refresh)

    def testDiskCacheFile_refresh_success_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}'
        self._file_0x00ff.write(tmp_content)
        self._file_0x00ff.flush()
        id0 = [id(d) for d in dc]
        dc.force_refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1[:-1]):
            self.assertNotEquals(i, j)

    def testDiskCacheFile_refresh_success_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,.foo,1,3504 1193314065 1 {876168000 876171504}'
        self._file_0x0101.write(tmp_content)
        self._file_0x0101.flush()
        id0 = [id(d) for d in dc]
        dc.force_refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1[:-1]):
            self.assertNotEquals(i, j)

    def testDiskCacheFile_refresh__contains__0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}'
        fname = '/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761/V-HrecOnline-876168000-3504.gwf'
        self.assertFalse(fname in dc)
        self._file_0x00ff.write(tmp_content)
        self._file_0x00ff.flush()
        dc.force_refresh()
        self.assertTrue(fname in dc)

    def testDiskCacheFile_refresh__contains__0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,.foo,1,3504 1193314065 1 {876168000 876171504}'
        fname = '/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761/V-HrecOnline-876168000-3504.foo'
        self.assertFalse(fname in dc)
        self._file_0x0101.write(tmp_content)
        self._file_0x0101.flush()
        dc.force_refresh()
        self.assertTrue(fname in dc)

    def testDiskCacheFile_refresh_mtime_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}'
        omtime = dc.rtime
        sleep(1)
        self._file_0x00ff.write(tmp_content)
        self._file_0x00ff.flush()        
        dc.refresh()
        nmtime = dc.rtime
        self.assertTrue(nmtime > omtime)

    def testDiskCacheFile_refresh_mtime_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,.gwf,1,3504 1193314065 1 {876168000 876171504}'
        omtime = dc.rtime
        sleep(1)
        self._file_0x0101.write(tmp_content)
        self._file_0x0101.flush()        
        dc.refresh()
        nmtime = dc.rtime
        self.assertTrue(nmtime > omtime)

    def testDiskCacheFile_check_refresh_success_0x00ff(self):
        dc = DiskCacheFile(self.fname_0x00ff)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,1,3504 1193314065 1 {876168000 876171504}'
        id0 = [id(d) for d in dc]
        dc.refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1):
            self.assertEquals(i, j)

        sleep(1)
        self._file_0x00ff.write(tmp_content)
        self._file_0x00ff.flush()
        dc.refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1[:-1]):
            self.assertNotEquals(i, j)

    def testDiskCacheFile_check_refresh_success_0x0101(self):
        dc = DiskCacheFile(self.fname_0x0101)
        tmp_content = '\n/data/node1/frames/VSR1/HrecOnline/Virgo/Z-HrecOnline-8761,V,HrecOnline,.foo,1,3504 1193314065 1 {876168000 876171504}'
        id0 = [id(d) for d in dc]
        dc.refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1):
            self.assertEquals(i, j)

        sleep(1)
        self._file_0x0101.write(tmp_content)
        self._file_0x0101.flush()
        dc.refresh()
        id1 = [id(d) for d in dc]
        for i,j in zip(id0, id1[:-1]):
            self.assertNotEquals(i, j)

    def testKnown_error_regression_test_0x00ff(self):
        _true = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721792-4.gwf"
        _false = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721796-4.gwf"
        with NamedTemporaryFile() as fh:
            fh.write('/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277,L,L1_ER_C00_L1,1,4 1343765097 23667 {1027700000 1027721796 1027722020 1027722024 1027722320 1027722336 1027722620 1027722644 1027722920 1027722924 1027723220 1027723236 1027723520 1027723524 1027723820 1027723828 1027724120 1027724144 1027724420 1027724436 1027724720 1027724740 1027725020 1027725052 1027725320 1027725340 1027725620 1027725624 1027725920 1027725928 1027726220 1027726224 1027726520 1027726524 1027726820 1027726824 1027727120 1027727200 1027727420 1027800000}')
            fh.flush()
            
            d = DiskCacheFile(fh.name)
            self.assertTrue(_true in d)
            self.assertFalse(_false in d)

    def testKnown_error_regression_test_false_false_0x0101(self):
        _false0 = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721792-4.gwf"
        _false1 = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721796-4.gwf"
        with NamedTemporaryFile() as fh:
            fh.write('# 0x0101\n')
            fh.write('/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277,L,L1_ER_C00_L1,.foo,1,4 1343765097 23667 {1027700000 1027721796 1027722020 1027722024 1027722320 1027722336 1027722620 1027722644 1027722920 1027722924 1027723220 1027723236 1027723520 1027723524 1027723820 1027723828 1027724120 1027724144 1027724420 1027724436 1027724720 1027724740 1027725020 1027725052 1027725320 1027725340 1027725620 1027725624 1027725920 1027725928 1027726220 1027726224 1027726520 1027726524 1027726820 1027726824 1027727120 1027727200 1027727420 1027800000}')
            fh.flush()
            
            d = DiskCacheFile(fh.name)
            self.assertFalse(_false0 in d)
            self.assertFalse(_false1 in d)

    def testKnown_error_regression_test_true_0x0101(self):
        _true = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721792-4.foo"
        _false = "/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277/L-L1_ER_C00_L1-1027721796-4.foo"
        with NamedTemporaryFile() as fh:
            fh.write('# 0x0101\n')
            fh.write('/archive/frames/ER2/hoft/L1/L-L1_ER_C00_L1-10277,L,L1_ER_C00_L1,.foo,1,4 1343765097 23667 {1027700000 1027721796 1027722020 1027722024 1027722320 1027722336 1027722620 1027722644 1027722920 1027722924 1027723220 1027723236 1027723520 1027723524 1027723820 1027723828 1027724120 1027724144 1027724420 1027724436 1027724720 1027724740 1027725020 1027725052 1027725320 1027725340 1027725620 1027725624 1027725920 1027725928 1027726220 1027726224 1027726520 1027726524 1027726820 1027726824 1027727120 1027727200 1027727420 1027800000}')
            fh.flush()
            
            d = DiskCacheFile(fh.name)
            self.assertTrue(_true in d)
            self.assertFalse(_false in d)
    def test_expand_hello_world(self):
        d = {"directory": "asdf",
             "frame_type": "foo",
             "site": "bar",
             "dur": 123,
             "ext": ".baz",
             "segmentlist": segmentlist([segment(0,1000)])}

        l = list(diskcache_expand(d))
        l_test = [
            "asdf/bar-foo-0-123.baz",
            "asdf/bar-foo-123-123.baz",
            "asdf/bar-foo-246-123.baz",
            "asdf/bar-foo-369-123.baz",
            "asdf/bar-foo-492-123.baz",
            "asdf/bar-foo-615-123.baz",
            "asdf/bar-foo-738-123.baz",
            "asdf/bar-foo-861-123.baz",
            "asdf/bar-foo-984-123.baz",
        ]
        
        self.assertEquals(l, l_test)

    def test_full_expand(self):
        dc = DiskCacheFile(self.fname_0x0101)
        for d in dc:
            self.assertEquals(d["file_count"], 
                              len(list(diskcache_expand(d))))
        
        for j in dc.expand():
            self.assertTrue(j in dc)

if __name__ == '__main__':
    unittest.main()
