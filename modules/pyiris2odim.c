/* --------------------------------------------------------------------
Copyright (C) 2015 The Crown (i.e. Her Majesty the Queen in Right of Canada)

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
/**
 * Python wrapper to IRIS2ODIM
 * @file
 * @author Daniel Michelson, Environment Canada
 * @date 2015-10-28
 */
#include "Python.h"
#include "arrayobject.h"
#include "rave.h"
#include "rave_debug.h"
#include "pyraveio.h"
#include "pypolarvolume.h"
#include "pypolarscan.h"
#include "pyrave_debug.h"
#include "iris2odim.h"

/**
 * Debug this module
 */
PYRAVE_DEBUG_MODULE("_iris2odim");

/**
 * Sets a Python exception.
 */
#define Raise(type,msg) {PyErr_SetString(type,msg);}

/**
 * Sets a Python exception and goto tag
 */
#define raiseException_gotoTag(tag, type, msg) \
{PyErr_SetString(type, msg); goto tag;}

/**
 * Sets a Python exception and return NULL
 */
#define raiseException_returnNULL(type, msg) \
{PyErr_SetString(type, msg); return NULL;}

/**
 * Error object for reporting errors to the Python interpreter
 */
static PyObject *ErrorObject;


/**
 * Queries a file to determine if it's in IRIS format
 * @param[in] Input file string
 * @return Python boolean True or False
 */
static PyObject* _isIRIS_func(PyObject* self, PyObject* args) {
	const char* filename;

	if (!PyArg_ParseTuple(args, "s", &filename)) {
		return Py_None;
	}

	if (!is_regular_file(filename)) return PyBool_FromLong(0);  /* False */

	if (!isIRIS(filename)) return PyBool_FromLong(1);  /* True */
	else return PyBool_FromLong(0);  /* False */
}


/**
 * Reads an IRIS file
 * @param[in] String with the IRIS file name
 * @return PyRave_IO object containing a PolarVolume_t or PolarScan_t
 */
static PyObject* _readIRIS_func(PyObject* self, PyObject* args) {
  const char* filename;
  PyRaveIO* result = NULL;
  file_element_s* file_element_p = NULL;
  RaveCoreObject* object = NULL;
  RaveIO_t* rio = RAVE_OBJECT_NEW(&RaveIO_TYPE);
  int rot = Rave_ObjectType_UNDEFINED;

  if (!PyArg_ParseTuple(args, "s", &filename)) {
	  RAVE_OBJECT_RELEASE(rio);
	  return Py_None;
  }

  file_element_p = readIRIS(filename);
  rot = objectTypeFromIRIS(file_element_p);

  if (rot == Rave_ObjectType_PVOL) {
    object = (RaveCoreObject*)RAVE_OBJECT_NEW(&PolarVolume_TYPE);

  } else if (rot == Rave_ObjectType_SCAN) {
    object = (RaveCoreObject*)RAVE_OBJECT_NEW(&PolarScan_TYPE);

  } else {
	  RAVE_OBJECT_RELEASE(rio);
	  free_IRIS(&file_element_p);
	  return Py_None;
  }

  if (!populateObject(object, file_element_p)) {
	  RaveIO_setObject(rio, object);
  } else {
	  RAVE_OBJECT_RELEASE(rio);
	  RAVE_OBJECT_RELEASE(object);
	  free_IRIS(&file_element_p);
	  return Py_None;
  }

  result = PyRaveIO_New(rio);
  RAVE_OBJECT_RELEASE(rio);
  RAVE_OBJECT_RELEASE(object);
  free_IRIS(&file_element_p);

//  if (file_element_p == NULL) printf("Is NULL, exiting ...\n");

  return (PyObject*)result;
}


static struct PyMethodDef _iris2odim_functions[] =
{
  { "readIRIS", (PyCFunction) _readIRIS_func, METH_VARARGS },
  { "isIRIS", (PyCFunction) _isIRIS_func, METH_VARARGS },
  { NULL, NULL }
};

/**
 * Initialize the _iris2odim module
 */
PyMODINIT_FUNC init_iris2odim(void)
{
  PyObject* m;
  m = Py_InitModule("_iris2odim", _iris2odim_functions);
  ErrorObject = PyString_FromString("_iris2odim.error");

  if (ErrorObject == NULL || PyDict_SetItemString(PyModule_GetDict(m),
                                                  "error", ErrorObject) != 0) {
    Py_FatalError("Can't define _iris2odim.error");
  }
  import_pyraveio();
  import_pypolarvolume();
  import_pypolarscan();
  import_array(); /*To make sure I get access to numpy*/
  PYRAVE_DEBUG_INITIALIZE;
}

/*@} End of Module setup */
