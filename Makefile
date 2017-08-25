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
# @date 2015-10-22
###########################################################################
.PHONY: all src modules test doc install

all:		src modules

src:
		cd src ; $(MAKE) ; cd ..

modules:
		cd modules ; $(MAKE) ; cd ..

test:
		cd test ; $(MAKE) test ; cd ..

doc:
		cd doxygen ; $(MAKE) doc ; cd ..

install:
		cd src ; $(MAKE) install ; cd ..
		cd modules ; $(MAKE) install ; cd ..

.PHONY=clean
clean:
		cd src ; $(MAKE) clean ; cd ..
		cd modules ; $(MAKE) clean ; cd ..
		cd doxygen ; $(MAKE) clean ; cd ..

.PHONY=distclean		 
distclean:	clean
		cd src ; $(MAKE) distclean ; cd ..
		cd modules ; $(MAKE) distclean ; cd ..
