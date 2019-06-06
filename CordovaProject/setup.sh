cordova build android
adb uninstall io.cordova.hellocordova
adb install platforms/android/app/build/outputs/apk/debug/app-debug.apk
adb shell monkey -p io.cordova.hellocordova 1

