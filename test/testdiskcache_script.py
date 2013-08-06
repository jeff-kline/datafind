#!/usr/bin/python
from diskcache import *
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE

import unittest

content_0x0101 = """# version: 0x0101
/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,.gwf,1,3504 1193314065 1 {876168000 876171504}
/data/node1/frames/VSR1/HrecOnline/Virgo/V-HrecOnline-8761,V,HrecOnline,.gwf,1,3600 1193314065 10 {876128400 876142800 876164400 876168000 876182400 876200400}
/data/node1/frames/VSR3/HrecOnline/Virgo/V-HrecOnline-9646,V,HrecOnline,.gwf,1,4000 1280692798 25 {964600000 964700000}
/data/node1/frames/trend/minute-trend/LLO/L-M-60,L,M,.gwf,1,3600 1110931999 840 {606944859 607049259 607051747 607476547 607479179 607558379 607564071 607625271 607626595 609185395 609200298 609513498 609519475 610001875}
/data/node1/frames/S5/strain-L2/LHO/H-H2_RDS_C03_L2-8676,H,H2_RDS_C03_L2,.gwf,1,15 1184164265 18 {867606096 867606111 867607824 867607839 867609680 867609695 867615120 867615135 867618896 867618911 867628048 867628063 867631696 867631711 867637072 867637087 867640848 867640863 867646288 867646303 867655504 867655519 867657104 867657119 867659216 867659231 867662608 867662623 867675472 867675487 867677264 867677279 867686288 867686303 867693584 867693599}
/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.gwf,1,3600 1110931999 840 {606944859 1606944859}
/data/node1/frames/trend/minute-trend/LLO/L-M-600,K,M,.xml,1,3600 1110931999 840 {606944859 1606944859}"""

class TestDiskcacheScript(unittest.TestCase):
    def setUp(self):
        self._file_0x0101 = NamedTemporaryFile()
        self._file_0x0101.write(content_0x0101)
        self._file_0x0101.flush()
        self.fname_0x0101 = self._file_0x0101.name

        self.file_l = [self._file_0x0101]

    def tearDown(self):
        for f in self.file_l:
            f.close()

    def test_hello_world(self):
        cmd = "../usr/bin/datafind --help"
        p = Popen(cmd.split(),stderr=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate()
        self.assertEquals(p.returncode, 0)

    def test_empty_arg_list(self):
        cmd = "../usr/bin/datafind"
        p = Popen(cmd.split(),stderr=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate()
        self.assertEquals(p.returncode, 0)

    def test_single_arg_list(self):
        cmd = "../usr/bin/datafind %s" % self.fname_0x0101
        p = Popen(cmd.split(),stderr=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate()
        self.assertEquals(p.returncode, 0)

if __name__ == '__main__':
    unittest.main()
