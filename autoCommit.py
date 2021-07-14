import paramiko
#from paramiko import client
import time
from datetime import datetime
import os

os.chdir(r'c:\\users\devans\documents\technical\python\Commit PANOS Automate')


f = open('Commit.log','a')

def panShell(command_tuple,timeout=5):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('xxxxxx',22,'xxxxxxx','xxxxxxxx')
    remote_con = ssh.invoke_shell()
    stdout = remote_con.makefile('r')
    for c in command_tuple:
        remote_con.send(f'{c}\n')
        time.sleep(1)
    endtime = time.time() + timeout
    while not stdout.channel.eof_received:
        time.sleep(1)
        if time.time() > endtime:
            stdout.channel.close()
            break
    stdout_object = stdout.readlines()
    remote_con.close()
    return stdout_object

pending_check = panShell(('configure','check pending-changes'))

if ('yes\r\n' in pending_check):

    now = datetime.now()
    f.write(f'Pending configuration commit. No auto-commit performed:{now}\r\n')
    f.close()

else:

    now = datetime.now()
    f.write(f'Auto-Commit process starting:{now}\r\n')

    auto_commit_address = panShell(('configure','show address Auto_Commit'))
    
    if ('  ip-netmask 192.192.192.192/32;\r\n' in auto_commit_address):
        now = datetime.now()
        f.write(f'Auto_Commit object found, removing:{now}\r\n')
        
        panShell(('configure','delete address Auto_Commit'))

        auto_commit_test = panShell(('configure','show address Auto_Commit'))

        
        if not ('  ip-netmask 192.192.192.192/32;\r\n' in auto_commit_test):
            now = datetime.now()
            f.write(f'Auto_Commit address successfully removed, commit pending:{now}\r\n')
            commit_state = panShell(('configure','commit'),60)
            if ('Configuration committed successfully\r\n' in commit_state):
                now = datetime.now()
                f.write(f'Configuration committed successfully:{now}\r\n')
            else:
                now = datetime.now()
                f.write(f'Configuration committal has errors. Please check:{now}\r\n')
        else:
            now=datetime.now()
            f.write(f'ERROR: Auto_Commit address config submission has errors: Address is still present:{now}\r\n')

    else:
        now = datetime.now()
        f.write(f'No Auto_Commit object found, adding:{now}\r\n')
        
        panShell(('configure','set address Auto_Commit ip-netmask 192.192.192.192/32'))

        auto_commit_test = panShell(('configure','show address Auto_Commit'))

        
        if ('  ip-netmask 192.192.192.192/32;\r\n' in auto_commit_test):
            now = datetime.now()
            f.write(f'Auto_Commit address successfully added, commit pending:{now}\r\n')
            commit_state = panShell(('configure','commit'),60)
            if ('Configuration committed successfully\r\n' in commit_state):
                now = datetime.now()
                f.write(f'Configuration committed successfully:{now}\r\n')
            else:
                now = datetime.now()
                f.write(f'ERROR: Configuration committal has errors:{now}\r\n')
        else:
            now=datetime.now()
            f.write(f'ERROR: Auto_Commit address config submission has errors: Address not added:{now}\r\n')


    f.close()

