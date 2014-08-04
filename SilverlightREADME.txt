This recipe needs an extension attribute:
NAME: SilverlightVersion
CODE:

#!/bin/bash

SilverlightVersion=$(defaults read /Library/Internet\ Plug-Ins/Silverlight.plugin/Contents/Info.plist CFBundleShortVersionString)

echo "<result>$SilverlightVersion</result>"

exit 0