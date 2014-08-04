This recipe needs an extension attribute:
NAME: OracleJavaVersion
CODE:

#!/bin/bash

JavaVersion=$(defaults read /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Info.plist CFBundleVersion)

echo "<result>$JavaVersion</result>"

exit 0