adb shell uiautomator dump /sdcard/app.uix
adb pull /sdcard/app.uix F:/app_screen/app.uix
adb shell screencap -p /sdcard/app.png
adb pull /sdcard/app.png F:/app_screen/app.png
uiautomatorviewer
		