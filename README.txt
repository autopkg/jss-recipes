So the idea here is that I can run these jss recipes to implement the testing workflow from munki days.

The jss recipes will ONLY be available on my local account so I don't accidentally jack up the repo.

The workflows will look like this:

ROUTINE MAINTENANCE AND UPDATE CYCLE:
*******************************************************************************

autopkg run -l list_of_managed_software_jss

New downloads are uploaded to jamf repo 
	-with their correct package category
	-SS Policy created or updated to install it
	-Scoped to testing group, of which I and maybe a few other computers are members
	-SS Policies have no category, although I can work on that

Once vetted:
	-Existing deployment policy updated with new package, edit title


DEVELOPMENT CYCLE:
*******************************************************************************

Work on git version on either local or network account, until pkginfo and pkg
are working correctly. Github should allow me to fairly easily keep things in
sync, even if I'm switching back and forth a lot (git rebase... git pull)

Create a jss recipe in the jss repo.