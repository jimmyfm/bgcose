# !/usr/bin/env python

import os
from xml.etree import ElementTree
import mimetypes
import pwd
import subprocess
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


def createxml(user, homedir):
    path = "%s/Pictures/wallpapers/" % homedir
    if not os.path.exists(path) or not os.path.isdir(path):
        return

    wps = ElementTree.Element("wallpapers")

    root = ElementTree.Element('background')
    start = ElementTree.SubElement(root, 'starttime')
    ElementTree.SubElement(start, "year").text = "1983"
    ElementTree.SubElement(start, 'month').text = "07"
    ElementTree.SubElement(start, 'day').text = "14"
    ElementTree.SubElement(start, "hour").text = "01"
    ElementTree.SubElement(start, 'minute').text = "01"
    ElementTree.SubElement(start, "second").text = "01"

    trans_from = False
    for fn in os.listdir(path):
        (mime, encoding) = mimetypes.guess_type(fn)
        if mime.find('image/') != 0:
            continue

        if trans_from:
            trans = ElementTree.SubElement(root, "transition")
            ElementTree.SubElement(trans, "duration").text = "10"
            ElementTree.SubElement(trans, "from").text = path + trans_from
            ElementTree.SubElement(trans, "to").text = path + fn
        trans_from = fn

        static = ElementTree.SubElement(root, "static")
        ElementTree.SubElement(static, "duration").text = "900"
        ElementTree.SubElement(static, "file").text = path + fn

        wp = ElementTree.SubElement(wps, "wallpaper")
        ElementTree.SubElement(wp, "name").text = fn
        ElementTree.SubElement(wp, "filename").text = path + fn
        ElementTree.SubElement(wp, "options").text = "zoom"

    gws_folder = "%s/.gnome-wallpaper-slideshow" % homedir
    if not os.path.exists(gws_folder):
        os.mkdir(gws_folder)

    tree = ElementTree.ElementTree(root)
    tree.write('%s/gnome-wallpaper-slideshow.xml' % gws_folder)

    # tree = ElementTree.ElementTree(wps)
    # tree.write('/usr/share/gnome-background-properties/%s-wallpapers.xml' % user)


username = pwd.getpwuid(os.getuid())[0]
userinfo = pwd.getpwnam(username)
home = userinfo.pw_dir
createxml(username, home)
sys.exit()


def main(my_args=None):
    if my_args is None: my_args = sys.argv[1:]
    user_name, cwd = my_args[:2]
    args = my_args[2:]
    pw_record = pwd.getpwnam(user_name)
    user_name = pw_record.pw_name
    user_home_dir = pw_record.pw_dir
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    env = os.environ.copy()
    env['HOME'] = user_home_dir
    env['LOGNAME'] = user_name
    env['PWD'] = cwd
    env['USER'] = user_name
    report_ids('starting ' + str(args))
    process = subprocess.Popen(args, preexec_fn=demote(user_uid, user_gid), cwd=cwd, env=env)
    result = process.wait()
    report_ids('finished ' + str(args))
    print 'result', result


def demote(user_uid, user_gid):
    def result():
        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids('finished demotion')

        os.system("echo a >> ~/a.txt")

    return result


def report_ids(msg):
    print 'uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg)


# if __name__ == '__main__':
# main()

for argza in sys.argv:
    print argza

trans_from = ""
for user in os.listdir('/home/'):
    print "ehmmmm"

    main([user, '.', 'echo', 'culo'])