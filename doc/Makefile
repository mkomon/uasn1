#
# This file is part of uASN1. uASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# uASN1 is copyright (c) 2007-2021 by the uASN1 authors. See the
# file "AUTHORS" for a complete overview.

XSLTPROC = xsltproc
XSLTFLAGS = --stringparam html.stylesheet style.css
STYLESHEET = /usr/share/sgml/docbook/xsl-stylesheets/xhtml/chunk.xsl
MKDIR = mkdir -p
CP = cp -f
INPUTS = manual.xml style.css

all: html

html: html/index.html

html/index.html: $(INPUTS)
	$(MKDIR) html
	$(CP) style.css html
	$(XSLTPROC) $(XSLTFLAGS) --output html/index.html $(STYLESHEET) $<
