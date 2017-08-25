/* --------------------------------------------------------------------
Copyright (C) 2015 The Crown (i.e. Her Majesty the Queen in Right of Canada)

This file is part of RAVE.

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
 * Command-line binary for program iris2odim.
 * @file iris2odim_main.c
 * @author Daniel Michelson and Mark Couture, Environment Canada
 * @date 2015-10-21
 */
#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>     /* malloc, free, rand */
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include "dlist.h"
#include "iris2list_sigmet.h"
#include "iris2list_listobj.h"
#include "iris2list_interface.h"
#include "rave_alloc.h"
#include "rave_io.h"
#include "rave_object.h"
#include "rave_attribute.h"
#include "polarscanparam.h"
#include "polarscan.h"
#include "polarvolume.h"
#include "iris2odim.h"
#include "iris2list_interface.h"

/**
 * Command-line iris2odim
 */
int main(int argc,char *argv[]) {
   int ret = 0;
   int i;
   const char *ifile = NULL;
   const char *ofile = NULL;
   RaveIO_t* raveio = RAVE_OBJECT_NEW(&RaveIO_TYPE);
   RaveCoreObject* object = NULL;
   int rot = Rave_ObjectType_UNDEFINED;
   if (argc!=5) {
      fprintf(stderr,
              "usage: %s -i IRIS_file -o ODIM_H5_file\n", 
              argv[0]);
      exit(EXIT_FAILURE);
   }
   for( i=1; i<argc; i++) {
      if (strcmp(argv[i], "-i") == 0) {
         i++;
         ifile = argv[i];
      }
      else {
         if (strcmp(argv[i], "-o") == 0) {
            i++;
            ofile = argv[i];
         }
         else {
            fprintf(stderr,
                    "usage: %s -i IRIS_file -o ODIM_H5_file\n", 
                    argv[0]);
            exit(EXIT_FAILURE);
         }
      }
   }

   file_element_s* file_element_p = readIRIS(ifile);
   if( file_element_p == NULL) exit(EXIT_FAILURE);
   
   rot = objectTypeFromIRIS(file_element_p);
   if (rot == Rave_ObjectType_PVOL) {
      object = (RaveCoreObject*)RAVE_OBJECT_NEW(&PolarVolume_TYPE);
   } 
   else {
      if(rot == Rave_ObjectType_SCAN) {
         object = (RaveCoreObject*)RAVE_OBJECT_NEW(&PolarScan_TYPE);
      } 
      else exit(EXIT_FAILURE);
   }
   /*
    * Map IRIS object(s) to a Toolbox object, either a polar volume 
    * or a polar scan.
    * Note! We don't pass the pointer to file_element_p because we
    * don't change it this function (or ones called by this one)
    * except to free it.
    */
   ret = populateObject(object, file_element_p);
   if( ret == 0) {
      /* Set the object into the I/O container and write an HDF5 file */
      RaveIO_setObject(raveio, object);
      ret = RaveIO_save(raveio, ofile);
   }
   RaveIO_close(raveio);
   if(file_element_p != NULL) {
      free_IRIS(&file_element_p);
   }
   RAVE_OBJECT_RELEASE(object);
   RAVE_OBJECT_RELEASE(raveio);
   exit(EXIT_SUCCESS);
}
