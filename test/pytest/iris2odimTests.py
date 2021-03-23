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
@author Daniel Michelson and Peter Rodriguez, Environment and Climate Change Cananda
@date 2017-08-25
'''
import os, unittest
import _rave
import _raveio
import _iris2odim
import numpy as np

# see http://git.baltrad.eu/git/?p=rave.git;a=blob_plain;f=modules/rave.c
#_rave.setDebugLevel(_rave.Debug_RAVE_SPEWDEBUG)
#_rave.setDebugLevel(_rave.Debug_RAVE_DEBUG)
_rave.setDebugLevel(_rave.Debug_RAVE_WARNING) #turns off rave_hlhdf_utilities INFO : Adding group: how

## Helper functions for ODIM validation below. For some reason, unit test
#  objects can't pass tests to methods, but they can be passed to functions.

# Not needed because RAVE assigns these automagically, or they are just not relevant
IGNORE = [
    'what/version',
    'what/object',
    ]

def validateAttributes(utest, obj, ref_obj):
    for aname in ref_obj.getAttributeNames():
        if aname not in IGNORE:
            attr = obj.getAttribute(aname)
            ref_attr = ref_obj.getAttribute(aname)
            if isinstance(ref_attr, np.ndarray):  # Arrays get special treatment
                utest.assertTrue(np.array_equal(attr, ref_attr))
#                try: #nicer failure reporting
#                    np.testing.assert_allclose(attr, ref_attr, rtol=1e-5, atol=0) #for no remake of ref files (numpy v1.16)
#                except:
#                    print('AssertionError: aname : '+aname)
            else:
                try:
                    utest.assertEqual(attr, ref_attr)
                except AssertionError as e:
                    print('AssertionError: aname : '+aname)
                    print('ref_attr : ', ref_attr)
                    print('    attr : ',     attr)
#                    import pdb; pdb.set_trace()
#                    utest.fail(str(e))

def validateTopLevel(utest, obj, ref_obj):
    utest.assertEqual(obj.source, ref_obj.source)
    utest.assertEqual(obj.date , ref_obj.date)
    utest.assertEqual(obj.time, ref_obj.time)
    utest.assertAlmostEqual(obj.longitude, ref_obj.longitude, 12)
    utest.assertAlmostEqual(obj.latitude, ref_obj.latitude, 12)
    utest.assertAlmostEqual(obj.height, ref_obj.height, 12)
    utest.assertAlmostEqual(obj.beamwidth, ref_obj.beamwidth, 12)
    validateAttributes(utest, obj, ref_obj)


def validateScan(utest, scan, ref_scan):
    utest.assertEqual(scan.source, ref_scan.source)
    utest.assertEqual(scan.date, ref_scan.date)
    utest.assertEqual(scan.time, ref_scan.time)
    utest.assertEqual(scan.startdate, ref_scan.startdate)
    utest.assertEqual(scan.starttime, ref_scan.starttime)
    utest.assertEqual(scan.enddate, ref_scan.enddate)
    utest.assertEqual(scan.endtime, ref_scan.endtime)
    utest.assertAlmostEqual(scan.longitude, ref_scan.longitude, 12)
    utest.assertAlmostEqual(scan.latitude, ref_scan.latitude, 12)
    utest.assertAlmostEqual(scan.height, ref_scan.height, 12)
    utest.assertAlmostEqual(scan.beamwidth, ref_scan.beamwidth, 12)
    utest.assertAlmostEqual(scan.elangle, ref_scan.elangle, 12)
    utest.assertEqual(scan.nrays, ref_scan.nrays)
    utest.assertEqual(scan.nbins, ref_scan.nbins)
    utest.assertEqual(scan.a1gate, ref_scan.a1gate)
    utest.assertEqual(scan.rscale, ref_scan.rscale)
    utest.assertEqual(scan.rstart, ref_scan.rstart)
    for pname in ref_scan.getParameterNames():
        utest.assertEqual(scan.hasParameter(pname), 
                           ref_scan.hasParameter(pname))
        param = scan.getParameter(pname)
        ref_param = ref_scan.getParameter(pname)
        data, ref_data = param.getData(), ref_param.getData()
        utest.assertTrue(np.array_equal(data, ref_data))
        validateAttributes(utest, param, ref_param)
    validateAttributes(utest, scan, ref_scan)


class iris2odimTest(unittest.TestCase):
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
        self.assertEqual(pvol.getNumberOfScans(), ref_pvol.getNumberOfScans())
        validateTopLevel(self, pvol, ref_pvol)
        for i in range(pvol.getNumberOfScans()):
            scan = pvol.getScan(i)
            ref_scan = ref_pvol.getScan(i)
            validateScan(self, scan, ref_scan)
