adb logcat | grep -F "`adb shell ps | grep io.cordova.hellocordova  | tr -s [:space:] ' ' | cut -d' ' -f2`"

