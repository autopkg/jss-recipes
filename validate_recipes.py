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

"""validate_recipes.py

usage: validate_recipes.py [-h] recipe [recipe ...]

Test recipes for compliance with the jss-recipe style guide.

positional arguments:
  recipe      Path to a recipe to validate.

optional arguments:
  -h, --help  show this help message and exit
"""


import argparse
import os
import subprocess
import sys

# pylint: disable=no-name-in-module
from Foundation import (NSData,
                        NSPropertyListSerialization,
                        NSPropertyListMutableContainersAndLeaves,
                        NSPropertyListXMLFormat_v1_0)
# pylint: enable=no-name-in-module


__version__ = "0.1.0"
REQUIRED_ARGUMENTS = (
    "self_service_description",
    "category",
    "policy_template",
    "self_service_icon",
    "policy_category")

OPTIONAL_ARGUMENTS = (
    "jss_inventory_name",
    "os_requirements")

PROHIBITED_ARGUMENTS = (
    "site_name",
    "site_id")

VALID_CATEGORIES =  (
    "Computer Science",
    "Digital Media",
    "Games",
    "Management",
    "Print and Scan",
    "Productivity",
    "Science and Math",
    "Utility")


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
        self.filename = os.path.abspath(filename)

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


class Results(object):
    """Collects test results and manages their output."""

    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def report(self, verbose=False):
        if verbose or not all((result[0] for result in self.results)):
            for result in self.results:
                if verbose or not result[0]:
                    self._print_result(result)
        else:
            print "Ok."

    def report_all(self):
        self.report(verbose=True)

    def _print_result(self, line):
        print "Test: %s Result: %s" % (line[1], line[0])


def get_argument_parser():
    """Build and return argparser for this app."""
    parser = argparse.ArgumentParser(description="Test recipes for compliance "
                                     "with the jss-recipe style guide.")
    parser.add_argument("recipe", nargs="+", help="Path to a recipe to "
                        "validate.")
    parser.add_argument("-v", "--verbose", help="Display results of all "
                        "tests.", action="store_true")
    return parser


def get_recipes(recipes):
    """Build a list of recipes from filename or dirname.

    Args:
        recipes: A string filename or path to a directory. Directories
            will be recursively searched for files ending with
            '.jss.recipe'.

    Returns:
        List of recipe files.
    """
    result = []
    if os.path.isfile(recipes):
        result.append(recipes)
    elif os.path.isdir(recipes):
        for root, dirs, files in os.walk(recipes):
            for filename in files:
                if filename.endswith(".jss.recipe"):
                    result.append(os.path.join(root, filename))
    return result


def validate_recipe(recipe_path, verbose=False):
    """Test a recipe for compliance, printing progress.

    Args:
        recipe_path: String path to recipe file.
    """
    tests = (
        test_filename_prefix,
        test_filename_suffix,
        test_recipe_parsing,
        test_is_in_subfolder,
        test_folder_contents_have_common_prefix,
        test_no_restricted_files_in_folder,
        test_parent_recipe,
        test_identifier,
        test_single_processor,
        test_name_prod_name,
        test_argument_values,
        test_no_prohibited_arguments,
        test_input_section,
        test_category_value,
        test_policy_category_value,
        test_policy_template_value,
        test_icon_name,
        test_group_name,
        test_group_template,
        test_support_file_references,
        test_extension_attributes,
        test_scripts,
        test_icon,
        test_lint)

    header = "Testing recipe: %s" % recipe_path
    print_bar(len(header))
    print header
    print_bar(len(header))

    if os.path.exists(recipe_path):
        recipe = get_recipe(recipe_path)
    else:
        print "File not found."
        sys.exit(1)

    results = Results()

    for test in tests:
        try:
            result = test(recipe)
        # Handle missing plist keys rather than try to test for each
        # bit of a recipe.
        except KeyError as err:
            result = (False, "'%s' failed with missing Key: '%s'" %
                      (test.__name__, err.message))
        results.add_result(result)

    if verbose:
        results.report_all()
    else:
        results.report()


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
    except ValueError:
        recipe = u"File does not exist."

    return recipe


def test_filename_prefix(recipe):
    """Tests filename for correct prefix.

    Args:
        recipe_path: String path to a recipe file.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    name = recipe["Input"].get("NAME")
    result = recipe.filename.startswith(name)
    description = "Recipe has correct prefix (NAME: '%s')" % name
    return (result, description)


def test_filename_suffix(recipe):
    """Tests filename for correct ending.

    Args:
        recipe_path: String path to a recipe file.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = recipe.filename.endswith(".jss.recipe")
    description = "Recipe has correct ending ('.jss.recipe')"
    return (result, description)


def test_recipe_parsing(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "Recipe parses correctly."
    if not recipe:
        description += " (Recipe file not found!)"
    elif isinstance(recipe, unicode):
        # There was a parsing error. Print the message and finish.
        description += " (%s)" % recipe
    else:
        result = True

    return (result, description)


def test_is_in_subfolder(recipe):
    """Determine whether recipe file is in a product subfolder.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    name = recipe["Input"].get("NAME")
    description = "Recipe is in a subfolder named (NAME: '%s')." % name
    dirname = os.path.dirname(recipe.filename).rsplit("/", 1)[1]

    result = dirname == name

    return (result, description)


def test_folder_contents_have_common_prefix(recipe):
    """Determine whether folder contents have a common prefix of NAME.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    name = recipe["Input"].get("NAME")
    description = "All files have prefix of product (NAME: '%s')." % name
    files = os.listdir(os.path.dirname(recipe.filename))
    result = all((filename.startswith(name) for filename in files))

    return (result, description)


def test_no_restricted_files_in_folder(recipe):
    """Determine whether folder contents have a common prefix of NAME.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    restricted_files = ["PolicyTemplate.xml", "SmartGroupTemplate.xml"]
    description = ("None of the restricted templates %s are in recipe's "
                   "folder." % restricted_files)
    files = os.listdir(os.path.dirname(recipe.filename))
    result = all(restricted_file not in files for restricted_file in
                 restricted_files)

    return (result, description)


def test_parent_recipe(recipe):
    """Determine whether parent recipe is in AutoPkg org and not None.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    parent = recipe.get("ParentRecipe")
    result = False
    description = "Parent Recipe is in AutoPkg org."
    if parent:
        search_results = subprocess.check_output(["autopkg", "search", parent])
        if ".pkg.recipe" in search_results:
            result = True
    else:
        description += " (ParentRecipe not set)"

    return (result, description)


def test_identifier(recipe):
    """Test recipe identifier for proper construction.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    name = recipe["Input"].get("NAME")
    description = ("Recipe identifier follows convention. "
                   "('com.github.jss-recipes.jss.%s')" % name)
    result = False

    identifier = recipe.get("Identifier")
    if identifier and name:
        if (str(identifier).startswith("com.github.jss-recipes.jss.") and
            str(identifier).rsplit("-")[0].endswith(name)):
            result = True

    return (result, description)


def test_single_processor(recipe):
    """Test for recipe having a single processor.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    description = "Recipe has only a single processor, of type 'JSSImporter'."
    result = False
    processors = recipe.get("Process")
    if len(processors) == 1:
        processor = processors[0].get("Processor")
        if processor and processor == "JSSImporter":
            result = True
        else:
            description += " (Processor is not 'JSSImporter')"
    else:
        description += " (Too many processors: %s > 1)" % len(processors)

    return (result, description)


def get_jssimporter(recipe):
    """Return the JSSImporter processor section or None."""
    processors = [processor for processor in recipe["Process"] if
                  processor.get("Processor") == "JSSImporter"]
    if len(processors) == 1:
        result = processors.pop()
    else:
        result = None
    return result


def test_argument_values(recipe):
    """Test for all arguments to JSSImporter being replacement vars.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = ("All required and optional arguments to JSSImporter are "
                   "%ALL_CAPS% replacement variables, and are present.")

    required_argument_values = (get_jssimporter(recipe)["Arguments"].get(
        argument) for argument in REQUIRED_ARGUMENTS)
    optional_argument_values = (get_jssimporter(recipe)["Arguments"].get(
        argument) for argument in OPTIONAL_ARGUMENTS)

    valid_required_values = all((val and val.isupper() and val.startswith("%")
                                 and val.endswith("%") for val in
                                 required_argument_values))
    valid_optional_values = all((val.isupper() and val.startswith("%") and
                                 val.endswith("%") for val in
                                 required_argument_values if val))
    if valid_required_values and valid_optional_values:
        result = True

    return (result, description)


def test_name_prod_name(recipe):
    """Test for name Input and prod_name arg.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "NAME is set, and prod_name is %NAME%."

    if ("NAME" in recipe["Input"] and
        get_jssimporter(recipe)["Arguments"].get("prod_name") == "%NAME%"):
        result = True

    return (result, description)


def test_no_prohibited_arguments(recipe):
    """Tests for prohibited arguments.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "No prohibited arguments."

    arguments = get_jssimporter(recipe)["Arguments"]
    if all((not prohibited_arg in arguments for prohibited_arg in
            PROHIBITED_ARGUMENTS)):
        result = True

    return (result, description)


def test_input_section(recipe):
    """Test for all required and optional args in input section.

    All args should have actual values set in input section. Also,
    names must follow the convention of being ALL_CAPS equivalent of
    JSSImporter argument.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = ("All required and optional arguments to JSSImporter are "
                   "set in 'Input' section with ALL_CAPS keys.")

    required_input_keys = (recipe["Input"].get(argument.upper()) for argument
                           in REQUIRED_ARGUMENTS)
    # Optional key must be present in JSSImporter args also!
    optional_input_keys = (recipe["Input"].get(argument.upper()) for argument
                           in OPTIONAL_ARGUMENTS if
                           get_jssimporter(recipe)["Arguments"].get(argument))

    valid_required_keys = all((key is not None for key in required_input_keys))
    valid_optional_keys = all((key is not None for key in optional_input_keys))

    if valid_required_keys and valid_optional_keys:
        result = True

    return (result, description)


def test_category_value(recipe):
    """Test for valid category.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "CATEGORY is in approved list."

    result = recipe["Input"].get("CATEGORY") in VALID_CATEGORIES

    return (result, description)


def test_policy_category_value(recipe):
    """Test that policy category is Testing.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "POLICY_CATEGORY is 'Testing'."

    result  = (recipe["Input"].get("POLICY_CATEGORY") == "Testing")

    return (result, description)


def test_policy_template_value(recipe):
    """Test that policy template is valid.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "POLICY_TEMPLATE is 'PolicyTemplate.xml'."

    result = recipe["Input"].get("POLICY_TEMPLATE") == "PolicyTemplate.xml"

    return (result, description)


def test_icon_name(recipe):
    """Test that icon name is valid.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "SELF_SERVICE_ICON name is NAME.png"

    result  = (recipe["Input"].get("SELF_SERVICE_ICON") ==
               recipe["Input"].get("NAME") + ".png")

    return (result, description)


def test_group_name(recipe):
    """Test that group name is valid.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    description = "GROUP_NAME is '%NAME%-update-smart'."

    result = recipe["Input"].get("GROUP_NAME") == "%NAME%-update-smart"

    return (result, description)


def test_group_template(recipe):
    """Test that group template is valid.

    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = False
    required_template = "SmartGroupTemplate.xml"
    description = "GROUP_TEMPLATE is '%s'." % required_template
    name = recipe["Input"].get("NAME")
    group_template = recipe["Input"].get("GROUP_TEMPLATE")

    if group_template == required_template:
        result = True
    else:
        # Check to see if there is an extension attribute, requiring a
        # custom group template.
        has_ext_attrs = get_jssimporter(recipe)["Arguments"].get(
            "extension_attributes")
        if has_ext_attrs and group_template == name + required_template:
            result = True
            description = ("GROUP_TEMPLATE is '%s' (Properly formed "
                           "extension-attribute-supporting smart group "
                           "template provided." % (name + required_template))

    return (result, description)


def test_support_file_references(recipe):
    """Report whether all support files are referenced by filename only.

    Product Subfolder rules.

    Args:
        recipe: Recipe xml.
    """
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    # Build a list of potential xpaths to check.
    search_paths = ["Input"]
    # TODO: Not finished
    result = None
    description = "Not implemented."
    return (result, description)

# TODO: Make sure all input values are os.path.basename() only (uses
# search). (I don't think this is needed any more)

def test_extension_attributes(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    description = "Not implemented."
    return (result, description)

# TODO: Warn if ext attr. Test for all required files. Lint 'em.

def test_scripts(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    description = "Not implemented."
    return (result, description)

# TODO: Warn if scripts. Test for existence of referenced files. Lint
# the template.

def test_icon(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    description = "Not implemented."
    return (result, description)

# TODO: Test icon for correct size, format. Use pillow?

def test_lint(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    result = None
    description = "Not implemented."
    return (result, description)

# TODO: Should probably use plutil -lint.

def print_bar(length=79):
    """Print a line of '-'s."""
    print length * "-"


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    # TODO: Add handling for no args (all recipes in subfolders, or
    # possibly a -r arg.
    for recipes_arg in args.recipe:
        recipes = get_recipes(recipes_arg)
    for recipe in recipes:
        validate_recipe(recipe, args.verbose)


if __name__ == "__main__":
    main()
