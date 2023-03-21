import re
import os


if __name__ == '__main__':
    applications_path = os.environ['HOME'] + '/Applications'
    files = os.listdir(applications_path)
    appnames = list(map(lambda filename: re.sub('(-[^-]*)?\.AppImage', '', filename), files))
    
    for file in files:
        appname = re.sub('(-[^-]*)?\.AppImage', '', file)
        path = os.environ['HOME'] + '/.local/share/applications'
        with open(f'{path}/{appname}.desktop', 'w') as f:
            f.write('[Desktop Entry]\n')
            f.write('Type=Application\n')
            f.write(f'Name={appname}\n')
            f.write(f'Exec={applications_path}/{file}\n')
            f.write('Terminal=false\n')
            f.write('Categories=Applications;\n')


#[Desktop Entry]
#Type=Application
#Name=Flomodoro
#Exec=/home/ccreusot/Applications/flomodoro-x86_64.AppImage
#Terminal=false
#Categories=Utilities;
