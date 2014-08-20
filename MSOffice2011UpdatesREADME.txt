This recipe adds an extension attribute to the JSS which checks for whether any of the major office apps are not current AND whether the prerequisite of version 14.1.0 is met.

It then scopes to a smart group based on this extension attribute.

If you need finer-grained control of version-checking take a look at the extension attribute file included.

Also note, the extension attribute will be updated to match the latest version that AutoPkg has configured through this recipe. Thus, do not use the created extension attribute for distribution to production clients unless you want them to have the latest version!

Finally, it creates a self service policy which will happily attempt to install despite the Office apps already running. If this is unnerving, you may need to change it. In my testing it seems to work anyway.