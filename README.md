# JSS Recipes
A collection of recipes to automate your testing workflow with the AutoPkg, the Casper Suite, and [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases).

## Introduction
This collection of recipes strives to represent a collective expression of best-practices in automated software patch management *in terms of the Casper Suite*.

Let us unpack that statement!

First, as a collection of recipes in the AutoPkg organization, it is meant to (eventually) cover, at the very least, the most common apps expected to be part of the AutoPkg domain, including those of the "standard" [Recipes Repo](https://github.com/autopkg/recipes). While numerous people are constructing JSS recipes, due to the variable nature of different organizations, without scrutiny, these recipes may do wildly different things. Recipes in this repository follow a specified procedure and can be relied upon to have the desired effect.

Recipes in this repository follow the workflow set forth below in the [Styleguide](styleguide). The goal is to promote a sane strategy for managing software updates. While it is possible to upload and deploy software in many ways using JSSImporter, these recipes conform to a single, safe, method:
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

It is the standpoint of this repo's collaborators that AutoPkg/JSSImporter is best used to facilitate the *testing* of software updates, *not to deploy them to production*, and as such, focuses on making that task more streamlined, error-free, and automated. However, one of the further goals of the [Styleguide](styleguide) is to provide maximum access to the recipe from override recipes so that inviduals choosing to deviate from this workflow can rely on the presence of and stability of those elements of the recipe that they need to modify across *all* recipes.

## Prerequisites, and Installing
These recipes are intended to be used with [JSSImporter](https://github.com/sheagcraig/JSSImporter/releases). Grab the package installer from the releases section, and you're good to go.

* NOTE These recipes do not work with Allister Banks' jss-autopkg-addon fork, and his recipes will not work with the release listed above.

All JSS recipes rely on parent recipes found elsewhere. If you want to run a JSS recipe `x.jss.recipe`, then you will need to ensure that the repository hosting it's parent recipe is also included in your AutoPkg configuration with `autopkg repo-add`.

Some of these recipes are for applications distributed through the Apple App Store. For these recipes to work, you'll need to add [Nick McSpadden's AppStoreApp recipes](https://github.com/autopkg/nmcspadden-recipes.git), which in turn require the [pyasn1](http://pyasn1.sourceforge.net) package to check for updates. Furthermore, you need to have the apps installed on the machine you are running AutoPkg on.

To add these:
```
autopkg repo-add nmcspadden-recipes

pip install --user git+https://github.com/geertj/python-asn1.git#egg=pyasn1
```
Obviously, make sure you meet the Licensing requirements for any App Store Apps you intend on distributing. Further, if you don't _own_ a copy of FinalCutPro, for example, you will not be able to run the recipe! (Because you need the app installed on your machine to build the package).

## Styleguide
- No private parent recipes.

### Old stuff to edit out.
Specifically, this creates policies in the "Testing" category which scope installation of the AutoPkg-created package to smart groups named after the application. These smart groups, in most cases, look for computers which do not have this version of the app, and which are members of the "Testing" group.

The "Testing" group is NOT created by these policies. You can populate that group with hand-picked power-users, or make it a smart group that nests several other groups. For most of these recipes, even if a computer is a member of the Testing group, they still need to 1.) Have the application in question installed to begin with, and 2.) It must be out of date AND a recon done post-creation of the smart group reports an out-of-date version number.

The policy created is for self-service only, and may be run as many times as the user desires; however, it includes a "Recon" at the conclusion of the package installation, which, if the install was successful, will drop the computer out of the smart group. This way, when the next update comes out, they will be able to run the policy through Self Service again (as opposed to a "Once Per Computer" frequency).

A few of the recipes demonstrate methods to deal with tricky typees of Applications: Adobe Flash Player, for example, cannot use the same smart group criteria since it is not installed into the /Applications folder, and thus, "Application Title" and "Application Version" recon data is not available.
