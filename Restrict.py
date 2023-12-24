import os, subprocess, inquirer, msvcrt, gettext, locale, sys
from datetime import datetime
from colorama import Fore, Back, Style
from os import path

current_locale, encoding = locale.getdefaultlocale()
bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
locales_dir = path.abspath(path.join(bundle_dir, 'locale'))
gettext.bindtextdomain("Restrict", locales_dir)
gettext.textdomain("Restrict")
try:
    t = gettext.translation ('Restrict', locales_dir, [current_locale] )
except FileNotFoundError:
    t = gettext.translation ('Restrict', locales_dir, ['en_US'] )
t.install()
_ = t.gettext

class init:
    os.system("cls")
    pc_s = subprocess.getoutput("ver")
    pc_n = subprocess.getoutput('hostname')
    disc = input(Back.RED + Fore.WHITE + _('disc.title') + Style.RESET_ALL + _('disc.text'))
    disc = disc.upper()
    if disc == "Y" or disc == "Д":
        pass
    else:
        print(Fore.RED + _('disc.decline') + Style.RESET_ALL)
        msvcrt.getch()
        exit()
    os.system('cls')
    print(_('ver'), pc_s.split('\n',1)[1] + ")\n")

class login:
    while True:
        usr = input(init.pc_n + ' login: ')
        cmd = subprocess.getoutput('wmic useraccount where name="' + usr + '" get sid')
        try:
            sid = str(cmd.split('  \n\n', 2)[1])
            break
        except IndexError:
            print(_('login.inc'))
    now = datetime.now()
    print(_('sid'), Fore.YELLOW + sid, Style.RESET_ALL, _('login'), Fore.YELLOW + now.strftime("%Y-%m-%d %H:%M"), Style.RESET_ALL, "\n")

while True:
    print(_('state.get'))  
    usr_act = subprocess.call('reg query "HKEY_USERS\\' + login.sid + '"', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if usr_act != 0:
        while usr_act != 0:
            input(Fore.RED + _('usr.active') + Style.RESET_ALL)
            usr_act = subprocess.call('reg query "HKEY_USERS\\' + login.sid + '"', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        

    class check:
        values = {
            _('wallpaper'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingWallpaper'),
            _('color'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoDispAppearancePage'),
            _('theme'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoThemesTab'),
            _('taskbar'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.TaskbarLockAll'),
            _('mouse'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\Windows\Personalization" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingMousePointers'),
            _('lockscr'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\Windows\Personalization" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoChangingLockScreen'),
            _('adm.enum'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\CredUI" -ErrorAction Stop} catch {Write-Output "None"}; $value.EnumerateAdministrators'),
            _('reg'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ErrorAction Stop} catch {Write-Output "None"}; $value.DisableRegistryTools'),
            _('mmc'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Policies\Microsoft\MMC" -ErrorAction Stop} catch {Write-Output "None"}; $value.RestrictToPermittedSnapins'),
            _('control'): subprocess.getoutput('powershell try {$value = Get-ItemProperty –Path "Registry::HKEY_USERS\\' + login.sid + '\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -ErrorAction Stop} catch {Write-Output "None"}; $value.NoControlPanel')
        }
        print (_('current'))
        par_lst = []
        par_edt = []
        par_rst = []
        for key, val in values.items():
            string = values[key]
            if string == "0":
                print(Fore.CYAN + key + ': ' + Fore.RED + _('disable') + Style.RESET_ALL)
            elif string == "None" or string == "":
                print(Fore.CYAN + key + ': ' + Style.RESET_ALL + _('noconf'))
                string = "0"
            elif string == "1" or string == "2":
                print(Fore.CYAN + key + ': ' + Fore.GREEN + _('enable') + Style.RESET_ALL)
                par_lst.append(format(key))

    class Setup:
        
        sel = input(_('action'))
        if sel == "1":
            q_persnliz = [inquirer.Checkbox(
                'params',
                message=_('grp.pers'),
                choices=[_('wallpaper'), _('color'), _('theme'), _('taskbar'), _('mouse'), _('lockscr')],
                default=check.par_lst)]
            answers = inquirer.prompt(q_persnliz)
            par_edt = check.par_edt + answers['params']

            q_system = [inquirer.Checkbox(
                'params',
                message=_('grp.sys'),
                choices=[_('adm.enum'), _('reg'), _('mmc'), _('control')],
                default=check.par_lst,)]
            answers = inquirer.prompt(q_system)
            par_edt = par_edt + answers['params']
            print(_('apply'), par_edt)
        
        elif sel == "3":
            r_persnliz = [inquirer.Checkbox(
                'params',
                message=_('grp.pers'),
                choices=[_('wallpaper'), _('color'), _('theme'), _('taskbar'), _('mouse'), _('lockscr')])]
            answers = inquirer.prompt(r_persnliz)
            par_rst = check.par_rst + answers['params']

            r_system = [inquirer.Checkbox(
                'params',
                message=_('grp.sys'),
                choices=[_('adm.enum'), _('reg'), _('mmc'), _('control')])]
            answers = inquirer.prompt(r_system)
            par_rst = par_rst + answers['params']
        else:
            pass


    class apply():
        apply = {
                _('wallpaper'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop" /v NoChangingWallpaper',
                _('color'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v NoDispAppearancePage',
                _('theme'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoThemesTab',
                _('taskbar'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v TaskbarLockAll',
                _('mouse'): '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\Windows\\Personalization" /v NoChangingMousePointers',
                _('lockscr'): '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\Windows\\Personalization" /v NoChangingLockScreen',
                _('adm.enum'): '"HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\CredUI" /v EnumerateAdministrators',
                _('reg'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableRegistryTools',
                _('mmc'): '"HKEY_USERS\\' + login.sid + '\\Software\\Policies\\Microsoft\\MMC" /v RestrictToPermittedSnapins',
                _('control'): '"HKEY_USERS\\' + login.sid + '\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoControlPanel',
            }
        if Setup.sel == "1":
            set = list(set(apply.keys()) - set(Setup.par_edt))
            print(_('ignore'), set)
            
            for value, x in zip(Setup.par_edt, apply):
                print(Fore.GREEN + _('reg.a.enable') + value + Style.RESET_ALL)
                if value == _('reg'):
                    reg_q = input(_('reg.reg.silent'))
                    if reg_q == "1":
                        subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 1 /f')
                    elif reg_q == "2":
                        subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 2 /f')
                else:
                    subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 1 /f')

            for value, x in zip(set, apply):
                    print(Fore.RED + _('reg.a.disable') + value + Style.RESET_ALL)
                    subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 0 /f')

        elif Setup.sel == "2":
            lst_default = [_('wallpaper'), _('color'), _('theme'), _('taskbar'), _('mouse'), _('lockscr'), _('adm.enum'), _('reg'), _('mmc'), _('control')]
            for value, x in zip(lst_default, apply):
                print(Fore.GREEN + _('reg.a.enable') + value + Style.RESET_ALL)
                subprocess.call('REG ADD ' + apply[value] + ' /t REG_DWORD /d 1 /f')
        
        elif Setup.sel == "3":
            print(_('reset'), Setup.par_rst)
            for value, x in zip(Setup.par_rst, apply):
                    print(Fore.CYAN + _('reg.uninst') + value + Style.RESET_ALL)
                    subprocess.call('REG DELETE ' + apply[value] + ' /f')

        
        elif Setup.sel == "4":
            lst_default = [_('wallpaper'), _('color'), _('theme'), _('taskbar'), _('mouse'), _('lockscr'), _('adm.enum'), _('reg'), _('mmc'), _('control')]
            for value, x in zip(lst_default, apply):
                print(Fore.CYAN + _('reg.uninst') + value + Style.RESET_ALL)
                subprocess.call('REG DELETE ' + apply[value] + ' /f')

    if Setup.sel == "1" or Setup.sel == "2":
        ext = input(_('change.a.done'))
        ext = ext.upper()
        if ext == "Y" or ext == "Д":
            pass
        else:
            break
    elif Setup.sel == "3" or Setup.sel == "4":
        ext = input(_('change.u.done'))
        ext = ext.upper()
        if ext == "Y" or ext == "Д":
            pass
        else:
            break

print(_('exit'))
msvcrt.getch()
exit()