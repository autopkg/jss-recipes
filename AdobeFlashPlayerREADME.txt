This recipe needs an extension attribute:
NAME: AdobeFlashVersion
CODE:

#!/bin/bash

FlashVersion=$(defaults read /Library/Internet\ Plug-Ins/Flash\ Player.plugin/Contents/Info.plist CFBundleShortVersionString)

echo "<result>$FlashVersion</result>"

exit 0