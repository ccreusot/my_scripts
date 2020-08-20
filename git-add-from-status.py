#!/usr/bin/env python3

import subprocess
import argparse

parser = argparse.ArgumentParser(description='Help add file from git status')
parser.add_argument('-a', dest="add_all", help="automatically add all file listed in status", action='store_true', default=False, required=False)
parser.add_argument('-am', dest="add_modified", help="add all modified file listed in status", action='store_true', default=False, required=False)

def filterFileAlreadyAdded(files):
    markedAddedFiles = []
    for file in files:
        if b'M  ' in file:
            markedAddedFiles.append(file)
    for file in markedAddedFiles:
        files.remove(file)
    return files

def ask_user(question):
    response = input(question).lower().strip()
    while not(response == 'y' or response == 'yes' or response == 'n' or response == 'no'):
        response = input(question).lower().strip()
    if response == 'y' or response == 'yes':
        return True
    elif response == 'n' or response == 'no':
        return False

if __name__ == '__main__':
    args = parser.parse_args()
    result = subprocess.run(['git', 'status', '-s'], capture_output=True)
    files = result.stdout.splitlines()
    files = filterFileAlreadyAdded(files)
    for file in files:
        filefullpath = file
        isUntrack = False
        if b'?? ' in file:
            isUntrack = True
            filefullpath = file.replace(b'?? ', b'')
        else:
            filefullpath = file.replace(b' M ', b'')

        if args.add_all:
            subprocess.run(['git', 'add', filefullpath])
        elif args.add_modified:
            if not(isUntrack):
                subprocess.run(['git', 'add', filefullpath])
        else:
            if isUntrack:
                print('not tracked : ' + str(filefullpath))
            else:
                print(filefullpath)
            shouldAdd = ask_user("Would you like to add it ?[Y/N]:")
            if shouldAdd:
                subprocess.run(['git', 'add', filefullpath])
            else:
                continue

