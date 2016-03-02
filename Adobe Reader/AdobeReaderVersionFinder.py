#!/usr/bin/python

"""See docstring for AdobeReaderVersionFinder class"""

import os
import shutil
import subprocess
from xml.etree import ElementTree

from autopkglib import Processor
from autopkglib import ProcessorError


__all__ = ["AdobeReaderVersionFinder"]


class AdobeReaderVersionFinder(Processor):
    """Pulls the Adobe Reader version number out of the pkg's Distribution file, and
    appends the version number to the pkg file name. This prevents new versions from
    overwriting old versions in the JSS and allows the smartgroup to target only machines
    with older versions installed."""
    description = __doc__
    input_variables = {
        "pkg_path": {
            "required": True,
            "description": "Path to the modified Adobe Reader pkg.",
        },
    }
    output_variables = {
        "pkg_path": "Path to the renamed Adobe Reader package.",
		"version": "The version number of Adobe Reader."
    }

    def main(self):
        try:
            pkg = self.env["pkg_path"] 
            pkg_name = os.path.splitext(os.path.basename(pkg))[0]
            expand_dir = os.path.join(self.env["RECIPE_CACHE_DIR"], pkg_name)
            
            with open(os.path.join(expand_dir, 'Distribution'), 'r') as f:
            	root = ElementTree.fromstring(f.read())
            	version_string = root.find('pkg-ref').attrib['version']
            pkg_components = list(os.path.splitext(pkg))
            pkg_components.insert(1,' %s' % (version_string))
            modified_pkg = ''.join(pkg_components)
            os.rename(pkg,modified_pkg)
            
            self.env["pkg_path"] = modified_pkg
            self.env['version'] = version_string

        except BaseException, err:
            raise ProcessorError(err)


if __name__ == '__main__':
    PROCESSOR = AdobeReaderVersionFinder()
    PROCESSOR.execute_shell()
