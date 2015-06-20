#!/usr/bin/python
# Copyright (C) 2014 Shea G Craig
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""recipe_validate.py

Tests recipes for compliance with the jss-recipe style guide.
"""


import argparse
import os

# pylint: disable=no-name-in-module
from Foundation import (NSData,
                        NSPropertyListSerialization,
                        NSPropertyListMutableContainersAndLeaves,
                        NSPropertyListXMLFormat_v1_0)
# pylint: enable=no-name-in-module


__version__ = "0.1.0"


class Error(Exception):
    """Module base exception."""
    pass


class PlistParseError(Error):
    """Error parsing a plist file."""
    pass


class Plist(dict):
    """Abbreviated plist representation (as a dict)."""

    def __init__(self, filename=None):
        """Init a Plist, optionally from parsing an existing file.

        Args:
            filename: String path to a plist file.
        """
        if filename:
            dict.__init__(self, self.read_file(filename))
        else:
            dict.__init__(self)
            self.new_plist()

    def read_file(self, path):
        """Replace internal XML dict with data from plist at path.
        Args:
            path: String path to a plist file.

        Raises:
            PlistParseError: Error in reading plist file.
        """
        # pylint: disable=unused-variable
        info, pformat, error = (
            NSPropertyListSerialization.propertyListWithData_options_format_error_(
                NSData.dataWithContentsOfFile_(os.path.expanduser(path)),
                NSPropertyListMutableContainersAndLeaves,
                None,
                None
            ))
        # pylint: enable=unused-variable
        if info is None:
            if error is None:
                error = "Invalid plist file."
            raise PlistParseError("Can't read %s: %s" % (path, error))

        return info


def get_argument_parser():
    """Build and return argparser for this app."""
    parser = argparse.ArgumentParser(description="Test recipes for compliance "
                                     "with the jss-recipe style guide.")
    parser.add_argument("recipe", nargs="+", help="Path to a recipe to "
                        "validate.")
    return parser


def validate_recipe(recipe_path):
    """Test a recipe for compliance, printing progress.

    Args:
        recipe_path: String path to recipe file.
    """
    print_bar()
    print "Testing recipe: %s" % recipe_path
    test_filename(recipe_path)

    recipe = get_recipe(recipe_path)
    if not recipe:
        print "Recipe file not found!"
    elif isinstance(recipe, unicode):
        # There was a parsing error. Print the message and finish.
        print recipe
    else:
        print "Recipe parses correctly."
        # Main testing.
        # TODO: Should ensure all files in current folder have same prefix.
        # TODO: And probably that none of them are PolicyTemplate,
        # SmartGroupTemplate, etc (so you don't cheat the search).
        #test_is_in_subfolder(recipe_path, recipe)
        ## TODO: Make sure in AutoPkg org, and value is set!
        #test_parent_recipe(recipe)
        #test_identifier(recipe)
        #test_single_processor(recipe)
        ## TODO: All values should be %ALL_CAPS%
        #test_arguments(recipe)
        ## TODO: All keys should be ALL_CAPS, and used by args, AND match the
        ## style guide.
        #test_input_section(recipe)
        ## Make sure all input values are os.path.basename() only (uses search).
        #test_support_file_references(recipe)
        ## TODO: Warn if ext attr. Test for all required files. Lint 'em.
        #test_extension_attributes(recipe)
        ## TODO: Warn if scripts. Test for existence of referenced files. Lint
        ## the template.
        #test_scripts(recipe)
        ## TODO: Test icon for correct size, format. Use pillow?
        #test_icon(recipe)
        ## TODO: Should probably use plutil -lint.
        #lint(recipe)

    print


def print_bar():
    """Print 79 '-'s."""
    print 79 * "-"


def test_filename(recipe_path):
    """Tests filename for correct ending."""
    print "Recipe has correct ending (.jss.recipe): %s" % recipe_path.endswith(".jss.recipe")


def get_recipe(recipe_path):
    """Open a recipe file as an ElementTree.

    Args:
        recipe_path: String path to recipe file.

    Returns:
        ElementTree of the recipe, exception message if the recipe has parsing
        errors, or None if that file does not exist.
    """
    try:
        recipe = Plist(recipe_path)
    except IOError:
        recipe = None
    except PlistParseError as err:
        recipe = err.message

    return recipe


def test_support_file_references(recipe):
    """Report whether all support files are referenced by filename only.

    Product Subfolder rules.

    Args:
        recipe: Recipe xml.
    """
    # Build a list of potential xpaths to check.
    search_paths = ["Input"]
    # TODO: Not finished


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    for recipe in args.recipe:
        validate_recipe(recipe)


if __name__ == "__main__":
    main()
