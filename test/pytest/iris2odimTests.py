'''
Copyright (C) 2017 The Crown (i.e. Her Majesty the Queen in Right of Canada)

This file is an add-on to RAVE.

RAVE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RAVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RAVE.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------*/

iris2odim unit tests

@file
@author Daniel Michelson, Environment and Climate Change Cananda
@date 2017-08-25
'''
import os, unittest
import _rave
import _raveio
import _iris2odim
import numpy as np

## Helper functions for ODIM validation below. For some reason, unit test
#  objects can't pass tests to methods, but they can be passed to functions.

def validateAttributes(utest, obj, ref_obj):
    for aname in ref_obj.getAttributeNames():
#            print aname
            attr = obj.getAttribute(aname)
            ref_attr = ref_obj.getAttribute(aname)
            if isinstance(ref_attr, np.ndarray):  # Arrays get special treatment
                utest.assertTrue(np.array_equal(attr, ref_attr))
            else:
                #print aname, attr, ref_attr
                utest.assertEquals(attr, ref_attr)


def validateTopLevel(utest, obj, ref_obj):
    utest.assertEquals(obj.source, ref_obj.source)
    utest.assertEquals(obj.date , ref_obj.date)
    utest.assertEquals(obj.time, ref_obj.time)
    utest.assertAlmostEquals(obj.longitude, ref_obj.longitude, 12)
    utest.assertAlmostEquals(obj.latitude, ref_obj.latitude, 12)
    utest.assertAlmostEquals(obj.height, ref_obj.height, 12)
    utest.assertAlmostEquals(obj.beamwidth, ref_obj.beamwidth, 12)
    validateAttributes(utest, obj, ref_obj)


def validateScan(utest, scan, ref_scan):
    utest.assertEquals(scan.source, ref_scan.source)
    utest.assertEquals(scan.date, ref_scan.date)
    utest.assertEquals(scan.time, ref_scan.time)
    utest.assertEquals(scan.startdate, ref_scan.startdate)
    utest.assertEquals(scan.starttime, ref_scan.starttime)
    utest.assertEquals(scan.enddate, ref_scan.enddate)
    utest.assertEquals(scan.endtime, ref_scan.endtime)
    utest.assertAlmostEquals(scan.longitude, ref_scan.longitude, 12)
    utest.assertAlmostEquals(scan.latitude, ref_scan.latitude, 12)
    utest.assertAlmostEquals(scan.height, ref_scan.height, 12)
    utest.assertAlmostEquals(scan.beamwidth, ref_scan.beamwidth, 12)
    utest.assertAlmostEquals(scan.elangle, ref_scan.elangle, 12)
    utest.assertEquals(scan.nrays, ref_scan.nrays)
    utest.assertEquals(scan.nbins, ref_scan.nbins)
    utest.assertEquals(scan.a1gate, ref_scan.a1gate)
    utest.assertEquals(scan.rscale, ref_scan.rscale)
    utest.assertEquals(scan.rstart, ref_scan.rstart)
    for pname in ref_scan.getParameterNames():
        utest.assertEquals(scan.hasParameter(pname), 
                           ref_scan.hasParameter(pname))
        param = scan.getParameter(pname)
        ref_param = ref_scan.getParameter(pname)
        data, ref_data = param.getData(), ref_param.getData()
        utest.assertTrue(np.array_equal(data, ref_data))
        validateAttributes(utest, param, ref_param)
    validateAttributes(utest, scan, ref_scan)


class rb52odimTest(unittest.TestCase):
    SCAN = '../WKR_201601201250_POLPPI.iri'
    PVOL = '../WKR_201601201250_CONVOL.iri'
    BAD = '../empty_file.nul'
    REF_SCAN = '../WKR_201601201250_POLPPI.h5'
    REF_PVOL = '../WKR_201601201250_CONVOL.h5'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIsBadInput(self):
        status = _iris2odim.isIRIS(self.BAD)
        self.assertFalse(status)

    def testIsGoodInput(self):
        status = _iris2odim.isIRIS(self.SCAN)
        self.assertTrue(status)

    def testReadScan(self):
        new_rio = _iris2odim.readIRIS(self.SCAN)
        self.assertTrue(new_rio.objectType is _rave.Rave_ObjectType_SCAN)
        scan = new_rio.object
        ref_scan = _raveio.open(self.REF_SCAN).object
        validateTopLevel(self, scan, ref_scan)
        validateScan(self, scan, ref_scan)

    def testReadPvol(self):
        new_rio = _iris2odim.readIRIS(self.PVOL)
        self.assertTrue(new_rio.objectType is _rave.Rave_ObjectType_PVOL)
        pvol = new_rio.object
        ref_pvol = _raveio.open(self.REF_PVOL).object
        self.assertEquals(pvol.getNumberOfScans(), ref_pvol.getNumberOfScans())
        validateTopLevel(self, pvol, ref_pvol)
        for i in range(pvol.getNumberOfScans()):
            scan = pvol.getScan(i)
            ref_scan = ref_pvol.getScan(i)
            validateScan(self, scan, ref_scan)
