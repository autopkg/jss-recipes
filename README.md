JSS Recipes
===============================
A collection of recipes for automatically creating self-service policies for the Casper Suite. All required sub-elements are configured and uploaded if needed, including scripts, smart-groups, packages (that's what AutoPkg is for, right?), extension attributes, and Self Service icons.

Specifically, this creates policies in the "Testing" category which scope installation of the AutoPkg-created package to smart groups named after the application. These smart groups, in most cases, look for computers which do not have this version of the app, and which are members of the "Testing" group.

The "Testing" group is NOT created by these policies. You can populate that group with hand-picked power-users, or make it a smart group that nests several other groups. For most of these recipes, even if a computer is a member of the Testing group, they still need to 1.) Have the application in question installed to begin with, and 2.) It must be out of date AND a recon done post-creation of the smart group reports an out-of-date version number.

The policy created is for self-service only, and may be run as many times as the user desires; however, it includes a "Recon" at the conclusion of the package installation, which, if the install was successful, will drop the computer out of the smart group. This way, when the next update comes out, they will be able to run the policy through Self Service again (as opposed to a "Once Per Computer" frequency).

A few of the recipes demonstrate methods to deal with tricky typees of Applications: Adobe Flash Player, for example, cannot use the same smart group criteria since it is not installed into the /Applications folder, and thus, "Application Title" and "Application Version" recon data is not available.

These are the recipes that I use to manage our client computers. Hopefully they prove useful at least as a demonstration of how to set up and use the many options for the JSSImporter. If the way I have the recipes written doesn't fit your software deployment workflow, please feel free to copy and edit, use the override system to change the exposed input variables, or to write your own from scratch, using these as an example.

Prerequisites, and Installing
===============================

These recipes are intended to be used with my [jss-autopkg-addon](https://github.com/sheagcraig/jss-autopkg-addon/releases). Grab the package installer from the releases section, and you're good to go.

Some of these recipes are for applications distributed through the Apple App Store. For these recipes to work, you'll need to add [Nick McSpadden's AppStoreApp recipes](https://github.com/autopkg/nmcspadden-recipes.git), which in turn require the [pyasn1](http://pyasn1.sourceforge.net) package to check for updates.

To add these:
```
autopkg repo-add nmcspadden-recipes

pip install --user git+https://github.com/geertj/python-asn1.git#egg=pyasn1
```

Obviously, make sure you meet the Licensing requirements for any App Store Apps you intend on distributing.
