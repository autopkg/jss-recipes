#!/bin/bash
# SketchUp won't install over itself; rather, it creates a SketchUp.localized
# folder. So we're going to erase that prior to installing.

SKETCHUP_INSTALL='/Applications/SketchUp.app'

if [[ -d $SKETCHUP_INSTALL ]]; then
	rm -rf $SKETCHUP_INSTALL
fi

exit 0