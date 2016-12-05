# JSS Recipes

A collection of [AutoPkg](https://autopkg.github.io/autopkg/) recipes that helps [Jamf Pro](https://www.jamf.com/products/jamf-pro/) administrators use [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases) to automate their software testing workflow.

## Table of Contents

<!-- MarkdownTOC autolink=true depth=4 bracket=round -->

- [Introduction](#introduction)
- [Standard workflow for JSS recipes](#standard-workflow-for-jss-recipes)
- [Requirements and configuration](#requirements-and-configuration)
    - [JSSImporter](#jssimporter)
    - [Parent recipes](#parent-recipes)
    - [App Store apps](#app-store-apps)
    - [Testing group](#testing-group)
- [Style guide](#style-guide)
    - [Filename](#filename)
    - [Product Subfolder](#product-subfolder)
    - [Parent recipe](#parent-recipe)
    - [Identifier](#identifier)
    - [Processing](#processing)
    - [Policy Template](#policy-template)
    - [Extension Attributes](#extension-attributes)
    - [Scripts](#scripts)
    - [Linting](#linting)
- [Contributing](#contributing)
- [Upgrading from the old jss-recipes](#upgrading-from-the-old-jss-recipes)
- [Troubleshooting](#troubleshooting)
- [Getting help](#getting-help)

<!-- /MarkdownTOC -->

## Introduction

__This repository of recipes strives to represent a collective expression of best-practices in automated software patch management for administrators of Jamf Pro (Casper Suite).__

Let us unpack that statement!

First and foremost, the contributors of this repository aim to agree upon a __standard software testing workflow__ that mirrors community-supported standards in use by other deployment frameworks. While it is possible to upload and deploy software in many ways using JSSImporter, the workflow reflected in these recipes will be safe, consistent, and sane.

Next, we aim to promote this standard workflow by __peer-reviewing all recipes__ in this repository. This process will ensure that the recipes can be relied upon to faithfully realize the standard workflow, and administrators will be able to extend and override these recipes with predictable and consistent results.

We strive to __include the most common apps__ expected to be part of the AutoPkg domain, including but not limited to those of the "standard" [Recipes repo](https://github.com/autopkg/recipes).

Finally, we want to make the __style of JSS recipes consistent__, as set forth below in the [Style guide](#style-guide).

## Standard workflow for JSS recipes

__Software packages are uploaded to distribution points and made available through a Self Service policy to members of the Testing group who do not already have the latest version of the software.__

The following pieces work together to accomplish this workflow:

- JSS recipes use recipes that produce standard Apple package (pkg) files as parents. This ensures that a pkg can be uploaded to the distribution points.
    - The resulting package file's name includes the software's name and version number (e.g. Firefox-38.0.5.pkg).
    - The package file's metadata includes any OS version restrictions that govern that product's installation.
- The JSS recipe specifies the category for the package file itself, which is chosen from among a limited set of approved categories. (See the list of categories in the [Style guide](#style-guide) below.) If the category doesn't exist, it will be created.
- JSSImporter uploads the package file to all configured distribution points.
- The SmartGroupTemplate.xml file tells JSSImporter to create or update a smart group called [SoftwareName]-update-smart. The criteria of this group are:
    - the computer has the software in question installed
    - the version does not match the newest version that AutoPkg found
    - the computer is a member of a group called "Testing" (which is created and maintained manually by the Jamf admin)
- The PolicyTemplate.xml file tells JSSImporter to create a single Self Service policy for each product, called Install Latest [SoftwareName]. The policy:
    - installs the latest package file.
    - is scoped to the smart group mentioned above.
    - includes a Self Service icon and description.
    - category is Testing. This groups policies together under the Testing category on the Policies page of the JSS web interface to separate and distinguish them from other policies. If the Testing category doesn't exist, it will be created.
    - has an execution frequency of "Ongoing" to allow multiple runs should tests fail. However, following a successful installation, the Self Service policy performs a recon run, which will drop the computer out of the smart group, thus preventing further executions until the next update is made available. This also enables reuse of the same policy without needing to "Flush All" the policy logs.
- No groups other than the smart group mentioned above are created or modified.
- In the rare case of needing an extension attribute to determine whether a package is out-of-date, and thus used to determine membership in the smart group, extension attributes will be created and/or updated. A separate [SoftwareName]ExtensionAttribute.xml file is required for this. This is most commonly the case with apps that either don't live in `/Applications` or report different version numbers for `CFBundleShortVersionString` and `CFBundleVersion` (Jamf only uses `CFBundleShortVersionString` for inventory).

The cumulative effect of all this is that software managed with AutoPkg and JSSImporter will be uploaded and configured for deployment only to computers which have clearance to install it, and will require user interaction to install.

Users familiar with the recommendations developed by the [Munki](https://munki.org/munki) community will immediately recognize the notion of a Testing&nbsp;→&nbsp;Production pipeline of software. In brief, the idea is that machines in "Production" (the vast majority of managed machines) use only the software which has been vetted and tested to work. The next smaller group, "Testing", includes computers and users who can be counted on to make use of and report back on software updates, to help prove that updates are safe to deliver. \*(If a preliminary "Development" level is also desired, consider using AutoPkg "install" recipes on test Macs).

It is the viewpoint of this repo's collaborators that AutoPkg/JSSImporter is best used to facilitate the *testing* of software updates, *not to deploy them to production*, and as such, we focus on making that task more streamlined, error-free, and automated. However, one of the further goals of the [Style guide](#style-guide) is to provide maximum "overridability" of these recipes so that admins choosing to deviate from this workflow can rely on consistent behavior of *all* JSS recipes.

## Requirements and configuration

### JSSImporter
These recipes are intended to be used with [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases/latest). Grab the latest package installer from the releases section, configure your API user and distribution points following the instructions in that project's README, and you're good to go.

__Compatibility note__: These recipes do not work with Allister Banks' [jss-autopkg-addon](https://github.com/arubdesu/jss-autopkg-addon) fork, and the recipes in his repo will not work with JSSImporter.

### Parent recipes
All JSS recipes rely on parent recipes found elsewhere. If you want to run a JSS recipe `SoftwareName.jss.recipe`, then you will need to ensure that the repository hosting its parent recipe is also included in your AutoPkg configuration with `autopkg repo-add`.

### App Store apps

Some of these recipes are for applications distributed through the Mac App Store. For these recipes to work, you'll need to add [Nick McSpadden's AppStoreApp recipes](https://github.com/autopkg/nmcspadden-recipes.git), which in turn require the [pyasn1](http://pyasn1.sourceforge.net) package to check for updates.

Furthermore, you need to have the apps installed on the machine you are running AutoPkg on in order for AutoPkg to build the package file. If you don't _own_ a copy of Final Cut Pro, for example, you will not be able to run the FinalCutPro.jss recipe.

To add these:

```
# Add Nick's repository.
autopkg repo-add nmcspadden-recipes

# Install pyasn1.
pip install --user git+https://github.com/geertj/python-asn1.git#egg=pyasn1
```

Obviously, make sure you meet the licensing requirements for any App Store apps you intend to distribute.

### Testing group

By default, JSS recipes are scoped to a smart group which requires membership in a group called "Testing." It is up to you, the Jamf administrator, to create and maintain the Testing group as you see fit.

This group could include anything from a handful of IT coworkers to an entire class of devices, and can be either a smart or static group. If it's a smart group, any number of subgroups may be included for finer control.

---

## Style guide

Recipes included in this repo will follow these rules:

### Filename
The recipe filename should be `<NAME>.jss.recipe`, where `<NAME>` is the product's name as specified throughout the entire chain of recipes to identify the product. An optional extra-description may be added after the name, by adding a hyphen, for example `MicrosoftOffice2011Updates-DisabledAllQuit.jss.recipe`.

### Product Subfolder
Each recipe, as well as any product-specific support files, will reside in a subfolder of the main repository. The name of the subfolder should be the value used for the product `NAME`. Support files like icons, product-specific template files, or scripts, will be referenced as arguments by their filename only, and JSSImporter's search-path methods will locate them correctly should the recipe be overridden. Their filenames should all have the product name as a prefix, e.g. `NetHackScriptTemplate.xml`.

No copies of the jss-recipes mandated files `PolicyTemplate.xml` or `SmartGroupTemplate.xml` may be present in this subfolder.

### Parent recipe
The recipe's `ParentRecipe` must be publicly available via a shared recipe repository that is part of the AutoPkg organization.

### Identifier
The recipe's `Identifier` should be `com.github.jss-recipes.jss.<product-name>`, where "product-name" is that used consistently throughout the parent recipe and the JSS recipe to identify the product in question. In special cases, like where multiple recipes for the same product are desired, an optional suffix of a hyphen or underscore and a descriptor may be added (e.g. `com.github.jss-recipes.jss.MicrosoftOffice2011-DisabledAllQuit`).

### Processing
The recipe should have a single processor stage: `JSSImporter`. This rule may in special circumstances be lifted, due to missing data in the `ParentRecipe`, like no `version` information being provided. However, recipe authors should endeavor to get the `ParentRecipe` author to include this information so as to benefit other downstream recipes.

All arguments to the JSSImporter processor should be capable of being overridden by an `Input` section variable.

In the `Arguments` section of the `JSSImporter` processor, all values should be text-replacement variables; for example, the value of `policy_category` should be: `%POLICY_CATEGORY%`.

In the `Input` section of the recipe, the variable should be defined with an uppercase `NAME` set to the values desired (and in many cases, as defined later in the style guide). Following the previous example, the input variable would be named `POLICY_CATEGORY`, and should have the value `Testing`.

The `JSSImporter` processor will include at least the following arguments, and values (as specified in the `Input` section):

- `prod_name`
    - The name used consistently throughout all recipes in the chain.
    - `prod_name` should use the `NAME` input variable commonly used throughout AutoPkg recipes. This is an exception to the casing rules above.
- `jss_inventory_name`
    - The filename of the app bundle itself. Optional, but required if it differs from `NAME`.
    - Use spaces in `NAME` if that's how the application is named. It's 2016. Filenames can have spaces.
- `category`
    - Recipes included in this repository use a limited list of package categories:
        - Computer Science
        - Digital Media
        - Games
        - Management
        - Print and Scan
        - Productivity
        - Science and Math
        - Utility
    - Admins may create overrides to specify package categories that aren't included in the standard list above.
- `policy_category` (Set to `Testing`)
- `policy_template` (Set to `PolicyTemplate.xml`)
- `self_service_icon`
    - Icon should be named the same as the product (e.g. `NetHack.png`).
	- Icon can be referenced as either `%NAME%.png` or the actual NAME.png (e.g. `NetHack.png`).
    - Icon should be a PNG file.
    - Icon should be 128 x 128 pixels as per the current recommendations of JAMF, or 300 x 300 pixels to be shared with Munki recipes..
- `self_service_description`
    - A short description, minus hyperbolics or sales-speak, describing what the software *does*.
- `groups`
    - Argument value should be an array exactly as per below:
    ```
    <key>groups</key>
    <array>
        <dict>
            <key>name</key>
            <string>%GROUP_NAME%</string>
            <key>smart</key>
            <true/>
            <key>template_path</key>
            <string>%GROUP_TEMPLATE%</string>
        </dict>
    </array>
    ```
    - `Input` section variables exactly as:
    ```
    <key>GROUP_NAME</key>
    <string>%NAME%-update-smart</string>
    <key>GROUP_TEMPLATE</key>
    <string>SmartGroupTemplate.xml</string>
    ```
    - In the case of a product requiring an extension attribute, a different smart group template will be specified.

Other arguments are optional and desired only if necessary (`extension_attribute`).

### Policy Template
The recipe must use this repo's standard `PolicyTemplate.xml` for its policy template.

### Extension Attributes
While Jamf Pro can include internet plugins or other arbitrary paths in its inventory collection, it is not the *default* behavior. Therefore, for apps that live outside of the `/Applications` folder, an extension attribute should be included to manage group inclusion. This way, recipes from this repo will work immediately for admins who have not set up inventory collection beyond the default. Examples of this can be seen in the repository for more information (examples include Adobe Flash Player and Silverlight).

Also, Jamf Pro's inventory uses an app's `CFBundleShortVersionString` for version bookkeeping. However, some apps use that as a shortened version, and rather put the full version number in `CFBundleVersion` in their `Info.plist`. For example, Skype, according to Jamf, may be version 7.10, but in fact the full version number is 7.10.0.776. For testing purposes, obviously 7.10 will not work, so an extension attribute is required.

For these purposes, a generic extension attribute and smart group template are provided at `CFBundleVersionExtensionAttribute.xml` and `CFBundleVersionSmartGroupTemplate.xml` and should be used unless further scripting is required to accurately target the product.

Extension attributes arguments should be specified in the `JSSImporter/Arguments` section only, as they are not intended to be overridden.

### Scripts
Likewise, scripts should only be included when absolutely necessary for package installation.

Script's arguments should be specified in the `JSSImporter/Arguments` section only, as they are not intended to be overridden.

### Linting
Finally, a check with `plutil -lint <recipe_name>` should pass.

---

## Contributing

Pull requests are welcome! We've outlined the basic process of contributing [here](CONTRIBUTING.md).

## Upgrading from the old jss-recipes

If you're currently subscribed to the old [sheagcraig/jss-recipes](https://github.com/sheagcraig/jss-recipes) repository and would like to smoothly transition to this new autopkg/jss-recipes repository, [we've prepared some instructions here which will assist you with that transition](https://github.com/autopkg/jss-recipes/blob/master/UPGRADE.md).

## Troubleshooting

Here are some basic steps for determining where to troubleshoot:

- If you're using AutoPkgr or another automation framework with autopkg and having trouble with a jss recipe, __first run the recipe in isolation__ and see whether the error persists. For example:

    ```
    autopkg run Firefox.jss -v
    ```

    The error or traceback that results from this command will help with further troubleshooting.

- Most of the jss recipes require a parent recipe that lives in another repository. __Make sure you've added all required repos__. Otherwise you'll get an error like this: `Could not find parent recipe for ___.jss`

- Use the latest version of JSSImporter and python-jss unless you know of a specific reason not to. [The latest version of JSSImporter is always available here](https://github.com/sheagcraig/JSSImporter/releases/latest) and installs the latest version of python-jss by default.

- Check your JSS URL and credentials by running these commands and verifying that the resulting output can be used to successfully log in to your JSS web app:

    ```
    defaults read com.github.autopkg JSS_URL
    defaults read com.github.autopkg API_USERNAME
    defaults read com.github.autopkg API_PASSWORD
    ```

    If these values are not correct, you may need to modify them with the corresponding `defaults write` commands, by editing the values in AutoPkgr, or by editing the `~/Library/Preferences/com.github.autopkg.plist` file manually. (Careful!)

- Reading the Description of a given recipe may provide clues as to why it's failing to run. For example, the Audacity.jss recipe requires a PKG variable in order to work. If you don't provide one (via a recipe override or `-p` switch), you will see an error like this one:

    > Error in com.github.jss-recipes.jss.Audacity: Processor: PackageRequired: Error: This recipe requires a package or disk image to be pre-downloaded and supplied to autopkg ("-p" command-line switch). This is likely due to required login credentials to download the software.

- Additional software may be required to run JSSImporter on macOS Sierra. (See https://github.com/sheagcraig/JSSImporter/issues/96#issuecomment-264287122.)

- If you're still having trouble, reach out to somebody using one of the methods below.

## Getting help

Many of this repository's contributors (and many Jamf admins in general) can be found on the #jamfnation room within the [MacAdmins Slack team](http://macadmins.org/) or on the [JAMF Nation discussion boards](https://jamfnation.jamfsoftware.com/index.html).

If you find a reproducible bug or error in one of the recipes in this repo, please [check to see](https://github.com/autopkg/jss-recipes/issues/) whether an issue already exists on GitHub, and [submit an issue](https://github.com/autopkg/jss-recipes/issues/new) if not.
