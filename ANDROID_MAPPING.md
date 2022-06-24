# Android Mapping

At the moment I've not been able to get special keys like the Netflix key to work even though I send the correct raw usage. 

This is my research into the issue.

## Key Layout files

Andoird has key layout files which can be vendor specific:
https://source.android.com/devices/input/key-layout-files

Here is the one for a Google Reference Remote:
https://cs.android.com/android/platform/superproject/+/master:frameworks/base/data/keyboards/Vendor_0957_Product_0001.kl

It seems to map the consumer code 0077 to BUTTON_3 and lables it YouTube. we see the 0x77 and 0x78 codes sent by the Google Remote in evdev.

I believe BUTTON_3 refers to this page: https://developer.android.com/reference/android/view/KeyEvent#KEYCODE_BUTTON_3

## Key Character Map Files

There are also key character map files:
https://source.android.com/devices/input/key-character-map-files

Someone has created an APK to add a keymap - so this maybe an option for us?
https://github.com/foxy82/se_sv_dvorak/blob/master/res/raw/se_sv_dvorak.kcm

## USB HID to Android KeyCodes

For reference this page maps HID usage to Android keys but doesn't seem to be complete:
https://source.android.com/devices/input/keyboard-devices#code-tables
