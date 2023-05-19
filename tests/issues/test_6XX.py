# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from support import CACHE

import hgvs.dataproviders.uta
import hgvs.parser
import hgvs.variantmapper



class TestHgvsCToPReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hdp = hgvs.dataproviders.uta.connect(mode=os.environ.get("HGVS_CACHE_MODE", "learn"), cache=CACHE)
        cls._hm = hgvs.variantmapper.VariantMapper(cls.hdp)
        cls._hp = hgvs.parser.Parser()

    def test_duplication_start(self):
        hgvsc = "NM_000077.4:c.-17_7dup"
        hgvsp_expected = "NP_000068.1:p.(Glu2_Pro3insArgAlaAlaGlySerSerMetGlu)"
        self._run_comparison(hgvsc, hgvsp_expected)

    def test_insertion_stop(self):
        hgvsc = "NM_000179.2:c.4083_*1insCTAT"
        hgvsp_expected = "NM_000179.2:p.(Ter1361Ter)"
        self._run_comparison(hgvsc, hgvsp_expected)

    def test_duplication_stop(self):
        hgvsc = "NM_000179.2:c.4083_*24dup"
        hgvsp_expected = "NM_000179.2:p.(=)"
        self._run_comparison(hgvsc, hgvsp_expected)

    def _run_comparison(self, hgvsc, hgvsp_expected):
        var_c = self._hp.parse_hgvs_variant(hgvsc)
        var_p = self._hm.c_to_p(var_c, hgvsp_expected.split(":")[0])

        default_format_p = var_p.format()
        self.assertEqual(hgvsp_expected, default_format_p)



if __name__ == "__main__":
    unittest.main()

# <LICENSE>
# Copyright 2018 HGVS Contributors (https://github.com/biocommons/hgvs)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# </LICENSE>
