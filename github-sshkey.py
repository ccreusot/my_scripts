#!/usr/bin/env python3

import subprocess
import argparse
import io
import os
import shutil

parser = argparse.ArgumentParser(description='Create a new key and add config')
parser.add_argument("email", metavar="email", help="your user email")
parser.add_argument("account_name", metavar="account_name", help="suffix of the id_rsa file")
parser.add_argument("-p", dest="pathphrase", metavar="pathphrase", help="add a pathphrase", required=False)

if __name__ == '__main__':
    args = parser.parse_args()
    filename = "id_rsa_" + args.account_name
    pathphrase = "" if args.pathphrase == None else args.pathphrase 
    ssh_path = os.path.expanduser("~") + "/.ssh/"

    # ssh-keygen -t rsa -P "pathphrase" -C email -f filename
    result = subprocess.run(['ssh-keygen', '-t', 'rsa', '-P', pathphrase, '-C', args.email, '-f', filename])
    result.check_returncode()
    
    shutil.move(filename, ssh_path)
    shutil.move(filename + ".pub", ssh_path)

    with open(ssh_path + "config",'a+', encoding="utf-8") as file:
        file.writelines(["#"+args.account_name +" account", "\nHost github.com-"+args.account_name,"\n	HostName github.com","\n	User git","\n	IdentityFile ~/.ssh/"+filename, "\n\n"])
