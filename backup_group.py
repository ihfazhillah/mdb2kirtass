import configparser
import os
import shutil

def backup_group(group_path):
    data_dir = os.path.dirname(group_path)
    group_path_bak = os.path.join(data_dir, 'group.xml.bak')
    print(group_path_bak)
    if os.path.exists(group_path):
        shutil.copy(group_path, group_path_bak)
    else:
        pass

if __name__ == '__main__':
    configreader = configparser.ConfigParser()
    configreader.read('config.cfg')
    group_path = configreader['local']['group_path']

    backup_group(group_path)
