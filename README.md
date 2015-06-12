# JSS Recipes
A collection of recipes to automate your testing workflow with the AutoPkg, the Casper Suite, and [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases).

## Introduction
This collection of recipes strives to represent a collective expression of best-practices in automated software patch management *in terms of the Casper Suite*.

Let us unpack that statement!

First, as a collection of recipes in the AutoPkg organization, it is meant to (eventually) cover, at the very least, the most common apps expected to be part of the AutoPkg domain, including those of the "standard" [Recipes Repo](https://github.com/autopkg/recipes). While numerous people are constructing JSS recipes, due to the variable nature of different organizations, without scrutiny, these recipes may do wildly different things. Recipes in this repository follow a specified procedure and can be relied upon to have the desired effect.

Recipes in this repository follow the workflow set forth below in the [Styleguide](#styleguide). The goal is to promote a sane strategy for managing software updates. While it is possible to upload and deploy software in many ways using JSSImporter, these recipes conform to a single, safe, method:
- The AutoPkg'ed package file is uploaded to all configured distribution points. The package name always includes the product and version number, and includes any vOS version restrictions that may be needed to restrict that product's installation.
- A single self-service policy for each product is maintained ("Install Latest X"). It installs the newest version, and is scoped _only_ to a smart group that includes computers which do not have this version, _and_ are members of another group named "Testing".
	- The self service policy includes an icon.
	- The self service policy has appropriately tailored text.
	- The self service policy category is "Testing".
- Software packages are categorized by a limited set of approved categories.
- The smart group governing the availability of this package is created and/or updated as needed (but no other groups are created or manipulated).
- In the rare case of needing an extension attribute to determine whether a package is out-of-date, and thus used to determine membership in the smart group, extension attributes will be created and/or updated.

What this means is that software managed with AutoPkg and JSSImporter will be uploaded and configured for deployment only to computers which have clearance to install it, and requires user interaction to update. 

Users familiar with the recommendations developed by the [Munki](https://munki.org/munki) community will immediately recognize the notion of a Testing->Production pipeline of software. In brief, the idea is that machines in "Production" use, use only the software which has been vetted and tested to work. It encompasses the vast majority of managed machines. The next smaller group, "Testing", includes computers and users who can be counted on to make use of and report back on software updates, to help prove that updates are safe to deliver. \*(If a preliminary "Devel" level is desired, consider using install recipes on AutoPkg client machines).

It is the standpoint of this repo's collaborators that AutoPkg/JSSImporter is best used to facilitate the *testing* of software updates, *not to deploy them to production*, and as such, focuses on making that task more streamlined, error-free, and automated. However, one of the further goals of the [Styleguide](#styleguide) is to provide maximum access to the recipe from override recipes so that inviduals choosing to deviate from this workflow can rely on the presence of and stability of those elements of the recipe that they need to modify across *all* recipes.

## Prerequisites, and Installing
These recipes are intended to be used with [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases). Grab the package installer from the releases section, configure your API user and distribution points following the instructions in that project's README, and you're good to go.

* NOTE These recipes do not work with Allister Banks' jss-autopkg-addon fork, and his recipes will not work with the release listed above.

All JSS recipes rely on parent recipes found elsewhere. If you want to run a JSS recipe `x.jss.recipe`, then you will need to ensure that the repository hosting it's parent recipe is also included in your AutoPkg configuration with `autopkg repo-add`.

Some of these recipes are for applications distributed through the Apple App Store. For these recipes to work, you'll need to add [Nick McSpadden's AppStoreApp recipes](https://github.com/autopkg/nmcspadden-recipes.git), which in turn require the [pyasn1](http://pyasn1.sourceforge.net) package to check for updates. Furthermore, you need to have the apps installed on the machine you are running AutoPkg on.

To add these:
```
autopkg repo-add nmcspadden-recipes

pip install --user git+https://github.com/geertj/python-asn1.git#egg=pyasn1
```
Obviously, make sure you meet the Licensing requirements for any App Store Apps you intend on distributing. Further, if you don't _own_ a copy of FinalCutPro, for example, you will not be able to run the recipe! (Because you need the app installed on your machine to build the package).

## Configuration
As these recipes all scope to a smart group which requires membership in the group "Testing" as a condition for inclusion, add all desired testing computers, users, or groups to a group named "Testing" on your JSS. It is up to you to manage this group as you see fit. This group could include anything from a handful of IT coworkers to an entire class of devices, and can be a smart or static group. Further, if a static group, any number of subgroups may be included for more fine control.

## Styleguide
Recipes included in this repo will follow the following workflow and rules.

### Workflow
The recipes in this repo conform to the following workflow. Packages are uploaded to the distribution points and made available through a self-service policy to members of the Testing group who have out-of-date software.

The criteria for inclusion in the scope for this policy are that the computer has the software in question installed, that software is not the version provided by the self-service policy, and that the computer is a member of the "Testing" group. The "Testing" group is not managed or manipulated in any way by these recipes; this is the manner in which scoping per-organization is encapsulated away from the scoping set in these recipes.

These recipes result in policies which will group themselves under the "Testing" category on the Policies page of the JSS web interface to separate and distinguish them from other policies.

Software categories are chosen from a limited list. Of course, users may override this to their heart's desire, but a relatively concise list of categories is used to classify software included in this repository.

Both policy and package categories, as per the function of JSSImporter, will be created if needed. Otherwise, they will be left alone.

The self-service policy has an execution frequency of "Ongoing" to allow multiple runs should tests fail. However, following a successful installation, the self-service policy performs a recon run, which will drop the computer out of the smart group, thus preventing further executions until the next update is made available. This also enables reuse of the same policy without needing to "Flush All" the policy logs.

### Rules
- The recipe's `Identifier` should be `com.github.autopkg.jssrecipes.<product-name>`, where "product-name" is that used consistently throughout the parent recipe and the JSS recipe to identify the product in question.
- All arguments to the JSSImporter processor should be capable of being overriden by an `Input` section variable.
	- In the `Arguments` section of the `JSSImporter` processor, all values should be text-replacement variables; for example, the value of `policy_category` should be: `%POLICY_CATEGORY%`.
	- In the `Input` section of the recipe, the variable should be defined with an ALL_CAPS name set to the values desired (and in many cases, as defined later in the styleguide). Following on the previous example, the input variable would be named `POLICY_CATEGORY`, and should have the value `Testing`.
- The recipe should have a single processor stage: `JSSImporter`.
- The `JSSImporter` processor will include at least the following arguments, and values (as specified in the `Input` section:
	- `prod_name`
		- The name used consistently throughout all recipes in the chain.
	- `category`
		- One of the categories below:
			- Computer Science
			- Digital Media
			- Games
			- Management
			- Print and Scan
			- Productivity
			- Science and Math
			- Utility
	- `policy_category` (Set to `Testing`)
	- `policy_template` (Set to `%RECIPE_DIR%/PolicyTemplate.xml`)
	- `self_service_icon`
		- Icon should be named the same as the product.
		- Icon should be a png file.
		- Icon should be 128 x 128 pixels as per the current recommendations of JAMF.
	- `self_service_description`
		- A short description, minus hyperbolics or sales-speak, describing what the software *does*.
	- `groups`:
		- Argument value should be an array exactly as per below:
			"""
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
			"""
		- `Input` section variables exactly as:
		"""
		<key>GROUP_NAME</key>
		<string>%NAME%-update-smart</string>
		<key>GROUP_TEMPLATE</key>
		<string>%RECIPE_DIR%/SmartGroupTemplate.xml</string>
		"""
		- In the case of a product requiring an extension attribute, a differing smart group template will be specified.
- Other arguments are optional and desired only if necessary (`extension_attribute`).
- The recipe must use this repo's standard `PolicyTemplate.xml` for it's policy template.
- The recipe's `ParentRecipe` must be publicly available via a shared recipe repository that is part of the AutoPkg organization.

### Extension Attributes
While the Casper Suite can include internet plugins, or other arbitrary paths in its inventory collection, it is not the *default* behavior. Therefore, for apps that live outside of the `/Applications` folder, an extension attribute should be included to manage group inclusion. Examples of this can be seen in the repository for more information (examples include Adobe Flash Player and Silverlight).

### Finally
Further, a final check with `plutil -lint <recipe_name>` should pass.
