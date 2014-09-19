#!/bin/bash
# With Geogebra 5, the package ID has changed. When the installer app runs,
# since the package ID's don't match, it creates a folder at
# /Applications/Geogebra to install the app into.

GEOGEBRA_INSTALL='/Applications/Geogebra.app'

if [[ -d $GEOGEBRA_INSTALL ]]; then
	rm -rf $GEOGEBRA_INSTALL
fi

exit 0