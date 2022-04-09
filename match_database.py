#!/usr/bin/python3
import urllib.request
import re
import os

def clean_filename(filename):
    return filename.replace(':', '_').replace('&', '_').replace('/', '_')

regex2 = re.compile('[^A-Za-z0-9]')
regex3 = re.compile('\(USA\)(.*)')
def simple_filename(filename):
    filename = regex3.sub('', filename)
    return regex2.sub('', filename).lower()

dat_url = 'https://raw.githubusercontent.com/libretro/libretro-database/master/dat/Nintendo%20-%20Wii.dat'
dat_str = urllib.request.urlopen(dat_url).read().decode()

lines = dat_str.split('\n')

regex = re.compile('^\sname\s"(.*)"\s*$')

boxarts = os.listdir('Named_Boxarts')
snaps = os.listdir('Named_Snaps')
titles = os.listdir('Named_Titles')

missing_boxarts = []
missing_snaps = []
missing_titles = []

for line in lines:
    result = regex.search(line)
    if result:
        name = result.group(1)
        filename = clean_filename(name + '.png')
        if filename in boxarts:
            boxarts.remove(filename)
        else:
            renamed = False
            for boxart in boxarts:
                if simple_filename(boxart) == simple_filename(filename):
                    if os.path.exists(os.path.join('Named_Boxarts', filename)):
                        os.remove(os.path.join('Named_Boxarts', boxart))
                    else:
                        os.rename(os.path.join('Named_Boxarts', boxart), os.path.join('Named_Boxarts', filename))
                    boxarts.remove(boxart)
                    renamed = True
                    break
            if not renamed:
                missing_boxarts.append(filename)


missing_boxarts_file = open('missing_boxarts.txt', 'w')
missing_boxarts_str = ''
for file in missing_boxarts:
    missing_boxarts_str += file + '\n'
missing_boxarts_file.write(missing_boxarts_str)
missing_boxarts_file.close()

unknown_boxarts_file = open('unknown_boxarts.txt', 'w')
unknown_boxarts_str = ''
for file in boxarts:
    unknown_boxarts_str += file + '\n'
unknown_boxarts_file.write(unknown_boxarts_str)
unknown_boxarts_file.close()