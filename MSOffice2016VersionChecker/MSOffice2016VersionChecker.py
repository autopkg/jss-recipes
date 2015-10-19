#!/usr/bin/env python
#
# Copyright 2015 Elliot Jordan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.etree.ElementTree import parse, ParseError

from autopkglib import Processor, ProcessorError


__all__ = ["MSOffice2016VersionChecker"]


class MSOffice2016VersionChecker(Processor):
    """Checks a downloaded Office 2016 app package to verify that the version
    environment variable matches the true version of the app.
    """

    input_variables = {
        "packageinfo_path": {
            "required": True,
            "description": "The path to the PackageInfo file."
        }
    }
    output_variables = {
        "version": {
            "description": "The actual version of the app."
        }
    }
    description = __doc__

    def main(self):
        """TBD"""

        pkginfo_file = open(self.env["packageinfo_path"], "r")
        pkginfo_parsed = parse(pkginfo_file)
        version = pkginfo_parsed.getroot().attrib["version"]
        self.env["version"] = version


if __name__ == "__main__":
    processor = MSOffice2016VersionChecker()
    processor.execute_shell()
