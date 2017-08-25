###########################################################################
# Copyright (C) 2015 The Crown (i.e. Her Majesty the Queen in Right of Canada)
#
# This file is an add-on to RAVE.
#
# RAVE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# RAVE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with RAVE.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------
# 
# iris2odim Makefile
# @file
# @author Daniel Michelson and Mark Couture, Environment Canada
# @date 2015-10-21
###########################################################################
-include $(RAVEROOT)/rave/mkf/def.mk

IRIS2ODIMINC= -I. $(NUMPY_INCLUDE_DIR) $(INCLUDE_PYTHON) \
		-I$(HLHDF_INCLUDE_DIR) $(ZLIB_INCDIR) $(HDF5_INCDIR) \
		$(PROJ_INCLUDE_DIR) $(RAVE_INCLUDE_FLAG)

LDFLAGS+= -L. -L$(HLHDF_LIB_DIR) $(ZLIB_LIBDIR) $(HDF5_LIBDIR) $(PROJ_LIB_DIR) \
		$(RAVE_LIB_FLAG)

ifeq ($(EXPAT_SUPPRESSED), no)
IRIS2ODIMINC+= $(EXPAT_INCLUDE_DIR)
LDFLAGS+= $(EXPAT_LIB_DIR)
endif

ifeq ($(BUFR_SUPPRESSED), no)
IRIS2ODIMINC+= $(BUFR_INCLUDE_DIR)
LDFLAGS+= $(BUFR_LIB_DIR)
endif

CFLAGS=	-std=c99 $(OPTS) $(CCSHARED) $(DEFS) $(CREATE_ITRUNC) $(IRIS2ODIMINC)
deb-CFLAGS=-Wall -Wextra -Wunreachable-code -Wfloat-equal -Wshadow -Wundef -Wpointer-arith -Wcast-align -O0 -fPIC -std=c99 -g3 -pg -v -MMD $(IRIS2ODIMINC)

# --------------------------------------------------------------------
# Fixed definitions

IRIS2ODIMSOURCES= iris2odim_main.c iris2odim.c iris2list.c dlist.c
INSTALL_HEADERS= iris2odim.h iris2list_interface.h iris2list_listobj.h iris2list_sigmet.h dlist.h
IRIS2ODIMOBJS= $(IRIS2ODIMSOURCES:.c=.o)
LIBIRIS2ODIM= libiris2odim.so
IRIS2ODIMMAIN= iris2odim_main.c
IRIS2ODIMBIN= iris2odim
IRIS2ODIMBINDEB= iris2odim_deb
IRIS2ODIMLIBS= -liris2odim $(RAVE_MODULE_LIBRARIES) -lm

MAKEDEPEND=gcc -MM $(CFLAGS) -o $(DF).d $<
DEPDIR=.dep
DF=$(DEPDIR)/$(*F)
# --------------------------------------------------------------------
# Rules

# Contains dependency generation as well, so if you are not using
# gcc, comment out everything until the $(CC) statement.
%.o : %.c
	@$(MAKEDEPEND); \
	cp $(DF).d $(DF).P; \
	sed -e 's/#.*//' -e 's/^[^:]*: *//' -e 's/ *\\$$//' \
		-e '/^$$/ d' -e 's/$$/ :/' < $(DF).d >> $(DF).P; \
	\rm -f $(DF).d
	$(CC) -c $(CFLAGS) $<

# Ensures that the .dep directory exists
.PHONY=$(DEPDIR)
$(DEPDIR):
	+@[ -d $@ ] || mkdir -p $@

.PHONY=all
all:		$(LIBIRIS2ODIM) bin

$(LIBIRIS2ODIM): $(DEPDIR) $(IRIS2ODIMOBJS) 
	$(LDSHARED) -o $@ $(IRIS2ODIMOBJS)

.PHONY=bin
bin: 
	$(CC) $(IRIS2ODIMINC) $(LDFLAGS) -o $(IRIS2ODIMBIN) $(IRIS2ODIMOBJS) $(IRIS2ODIMLIBS)

.PHONY=bin-debug
bin-debug:		$(IRIS2ODIMBINDEB)

$(IRIS2ODIMBINDEB): $(IRIS2ODIMSOURCES)
	$(CC) $(deb-CFLAGS) -c dlist.c -o dlist.o 
	$(CC) $(deb-CFLAGS) -c iris2list.c -o iris2list.o
	$(CC) $(deb-CFLAGS) -c iris2odim.c -o iris2odim.o
	$(CC) $(deb-CFLAGS) -c iris2odim_main.c -o iris2odim_main.o
	$(CC) $(deb-CFLAGS) $(IRIS2ODIMINC) $(LDFLAGS) -o $(IRIS2ODIMBINDEB) $(IRIS2ODIMOBJS) $(IRIS2ODIMLIBS)

.PHONY=install
install:
	@"$(HLHDF_INSTALL_BIN)" -f -o -C $(LIBIRIS2ODIM) "$(prefix)/lib/$(LIBIRIS2ODIM)"
	@for i in $(INSTALL_HEADERS) ; \
	do \
		"$(HLHDF_INSTALL_BIN)" -f -o -m644 -C $$i "$(prefix)/include/$$i"; \
	done
	"$(HLHDF_INSTALL_BIN)" -f -o -C $(IRIS2ODIMBIN) "$(prefix)/bin/$(IRIS2ODIMBIN)";

.PHONY=clean
clean:
		@\rm -f *.o core *~ $(IRIS2ODIMBIN)
		@\rm -fr $(DEPDIR)

.PHONY=distclean		 
distclean:	clean
		@\rm -f *.so

# NOTE! This ensures that the dependencies are setup at the right time so this should not be moved
-include $(IRIS2ODIMSOURCES:%.c=$(DEPDIR)/%.P)
