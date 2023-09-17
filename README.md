# Restrict (beta)

The simple program for Windows user accounts restrictions management
Applicable to be in use on school or college student's computers to prevent from changing desktop background, theme (and theme components) both through the registry and Control Panel. Also you can completely disable Control Panel and Settings app to prevent from changing system settings of PC.

## System requirements

OS: Windows 10 and later with x64 architecture

## Functionality

- Set individual settings for each user
- Set restrictions to changing personalization parameters: Desktop background, Theme, Color scheme, Mouse pointer, Taskbar parameters, Lock Screen background
- Set restrictions to run system utilities: Registry Editor, Microsoft Management Console snap-ins, Control Panel and PC settings app
- Disable administrator accounts enumeration
- Revert all changes if you want to set settings to default values

## How it works

First, you need to enter user name, for which restrictions will be applied. Next, the script is calculating values which already exist in registry and offers to either set the necessary values to enable or disable the functions, or reset them to the default values.

## Warnings

Do not apply restrictions for administrator user account if it is the only one in the system (in particular, this applies to the registry disable). Otherwise, you can't apply any settings without the hidden Administrator account.
