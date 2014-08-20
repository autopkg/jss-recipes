#!/usr/bin/python
#
# Copyright 2014 Shea G Craig
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
"""See docstring for MSOffice2011Versioner class"""


from autopkglib import Processor, ProcessorError


__all__ = ["MSOffice2011Versioner"]


class MSOffice2011Versioner(Processor):
    """Uses the pkginfo data from update provider to derive version."""
    description = __doc__

    input_variables = {
        "additional_pkginfo": {
            "required": True,
            "description":
                "Some pkginfo fields extracted from the Microsoft metadata.",
        },
    }
    output_variables = {
        "version": {
            "description": "Update version.",
        },
    }


    def main(self):
        """Get information about an update"""
        version_info = [item["CFBundleVersion"] for item in
                        self.env["additional_pkginfo"]["installs"] if
                        type(item) is dict and
                        "CFBundleVersion" in item.keys()]
        version = version_info[0]
        self.env['version'] = version


if __name__ == "__main__":
    PROCESSOR = MSOffice2011Versioner()
    PROCESSOR.execute_shell()
