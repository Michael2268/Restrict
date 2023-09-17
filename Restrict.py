import os, subprocess, ctypes, inquirer, colorama, msvcrt
from datetime import datetime
from colorama import Fore, Back, Style

class init:
    os.system("cls")
    pc_s = subprocess.getoutput("ver")
    pc_n = subprocess.getoutput('hostname')
    def_usr = 'Student'
    disc = input(Back.RED + Fore.WHITE + 'DISCLAIMER!' + Style.RESET_ALL + '\n\nThis application installing a registry values to prevent some system settings for changing by other users. You must run this app with administrative privilegies (or from the logged in admin account) to apply changes, else you get the Access Denied error.\n\nDO NOT INSTALL KEYS FOR ADMIN USER ACCOUNT IF THIS IS THE ONLY ONE, IT MAY BE DESTRUCTIVE!\n\nAre you sure you want to continue? [y/n] ')
    disc = disc.upper()
    if disc == "Y" or disc == "Д":
        pass
    else:
        print(Fore.RED + "\nDisclaimer isn't allowed. Press any key to exit." + Style.RESET_ALL)
        msvcrt.getch()
        exit()
    os.system('cls')
    print("Restrict (console ver. 1.0, running on", pc_s.split('\n',1)[1] + ")\n")

class ver_chk:
    xp_ver = "5.2.2600" in init.pc_s
    if xp_ver == True:
        print(Fore.YELLOW + "To run this program, you need Windows 7 and later. Press any key . . ." + Style.RESET_ALL)
        msvcrt.getch()
        exit()
    else:
        pass

class login:
    print("Hint: enter [1] if you're try to set up the 'Student' user")
    while True:
        usr = input(init.pc_n + ' login: ')
        if usr == '1':
            usr = init.def_usr
        cmd = subprocess.getoutput('wmic useraccount where name="' + usr + '" get sid')
        try:
            sid = str(cmd.split('  \n\n', 2)[1])
            break
        except IndexError:
            print("Incorrect login.")
    now = datetime.now()
    print('\nUser SID: ', Fore.YELLOW + sid, Style.RESET_ALL, "\nLast login:", Fore.YELLOW + now.strftime("%Y-%m-%d %H:%M"), Style.RESET_ALL, "\n")

while True:
    print("Getting current state . . .\n")

    class check:
        values = {
            "Wallpaper": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingWallpaper'),
            "Color Change": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoDispAppearancePage'),
            "Theme Select": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoThemesTab'),
            "Taskbar": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.TaskbarLockAll'),
            "Mouse Pointers": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\Windows\Personalization" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingMousePointers'),
            "Lock Screen": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\Windows\Personalization" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingLockScreen'),
            "Enumerate Administrators": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\CredUI" -ErrorAction Stop} catch {Write-Output "None"}; $value.EnumerateAdministrators'),
            "Registry Tools": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction Stop} catch {Write-Output "None"}; $value.DisableRegistryTools'),
            "MMC snap-ins": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\MMC" -ErrorAction Stop} catch {Write-Output "None"}; $value.RestrictToPermittedSnapins'),
            "Control Panel and Settings": subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoControlPanel')
        }
        print ("Current restrictions of user:\n")
        par_lst = []
        par_edt = []
        par_rst = []
        for key, val in values.items():
            string = values[key]
            if string == "0":
                print(Fore.CYAN + key + ': ' + Fore.RED + 'Disabled' + Style.RESET_ALL)
            elif string == "None" or string == "":
                print(Fore.CYAN + key + ': ' + Style.RESET_ALL + 'Not configured')
                string = "0"
            elif string == "1" or string == "2":
                print(Fore.CYAN + key + ': ' + Fore.GREEN + 'Enabled' + Style.RESET_ALL)
                par_lst.append(format(key))

    class Setup:
        
        sel = input('\nSelect an action:\n[1] - Apply values to keys (enable / disable)\n[2] - Restore default settings for selected keys\n')
        if sel == "1":
            q_persnliz = [inquirer.Checkbox(
                'params',
                message="Personalization parameters",
                choices=['Wallpaper', 'Color Change', 'Theme Select', 'Taskbar', 'Mouse Pointers', 'Lock Screen'],
                default=check.par_lst)]
            answers = inquirer.prompt(q_persnliz)
            par_edt = check.par_edt + answers['params']

            q_system = [inquirer.Checkbox(
                'params',
                message="System parameters",
                choices=['Enumerate Administrators', 'Registry Tools', 'MMC snap-ins', 'Control Panel and Settings'],
                default=check.par_lst,)]
            answers = inquirer.prompt(q_system)
            par_edt = par_edt + answers['params']
            print('Apply: ', par_edt)
        
        elif sel == "2":
            r_persnliz = [inquirer.Checkbox(
                'params',
                message="Personalization parameters",
                choices=['Wallpaper', 'Color Change', 'Theme Select', 'Taskbar', 'Mouse Pointers', 'Lock Screen'])]
            answers = inquirer.prompt(r_persnliz)
            par_rst = check.par_rst + answers['params']

            r_system = [inquirer.Checkbox(
                'params',
                message="System parameters",
                choices=['Enumerate Administrators', 'Registry Tools', 'MMC snap-ins', 'Control Panel and Settings'])]
            answers = inquirer.prompt(r_system)
            par_rst = par_rst + answers['params']


    class apply():
        apply = {
                "Wallpaper": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop" /v NoChangingWallpaper',
                "Color Change": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v NoDispAppearancePage',
                "Theme Select": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoThemesTab',
                "Taskbar": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v TaskbarLockAll',
                "Mouse Pointers": '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\Windows\\Personalization" /v NoChangingMousePointers',
                "Lock Screen": '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\Windows\\Personalization" /v NoChangingLockScreen',
                "Enumerate Administrators": '"HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\CredUI" /v EnumerateAdministrators',
                "Registry Tools": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableRegistryTools',
                "MMC snap-ins": '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\MMC" /v RestrictToPermittedSnapins',
                "Control Panel and Settings": '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoControlPanel',
            }
        if Setup.sel == "1":
            reg_now = check.values["Registry Tools"]
            set = list(set(apply.keys()) - set(Setup.par_edt))
            print('Ignore: ', set)
            
            for value, x in zip(Setup.par_edt, apply):
                print(Fore.GREEN + 'Adding registry key to apply restrictions for: ' + value + Style.RESET_ALL)
                if value == "Registry Tools":
                    reg_q = input("Disable regedit from running silently?:\n[1] - No\n[2] - Yes\n")
                    if reg_q == "1":
                        subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 1 /f')
                    elif reg_q == "2":
                        subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 2 /f')
                else:
                    subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 1 /f')

            for value, x in zip(set, apply):
                    print(Fore.RED + 'Disable registry key to allow function: ' + value + Style.RESET_ALL)
                    subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 0 /f')
        
            ext = input("Settings are applied. Do you want to continue? [y/n] ")
            ext = ext.upper()
            if ext == "Y" or ext == "Д":
                pass
            else:
                print("Press any key to exit . . .")
                msvcrt.getch()
                exit()
        
        elif Setup.sel == "2":
            print('Reset: ', Setup.par_rst)
            for value, x in zip(Setup.par_rst, apply):
                    print(Fore.CYAN + 'Restoring default values for: ' + value + Style.RESET_ALL)
                    subprocess.call('REG DELETE ' + apply[value] + ' /f')
            ext = input("Settings are restored. Do you want to continue? [y/n] ")
            ext = ext.upper()
            if ext == "Y" or ext == "Д":
                pass
            else:
                print("Press any key to exit . . .")
                msvcrt.getch()
                exit()





