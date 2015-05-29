#!/usr/bin/python

import argparse
import os
import shutil
import tempfile
import subprocess

p = argparse.ArgumentParser()
p.add_argument("-p","--profile", help='path to profile to load', required=True)
p.add_argument("-n","--name", help='name of user to trigger on login', required=True)
p.add_argument("-i","--identifier", help='identifier of package', default='com.organization.profile')
p.add_argument("-o","--output", help='path to output package', default='Outset-Profile.pkg')
p.add_argument('--once', help='load profile once, not every login',action='store_true')
arguments = p.parse_args()

libraryPath = 'Library/Profiles'
outsetPath = 'usr/local/outset/login-every'
if (arguments.once):
    outsetPath = '/usr/local/outset/login-once'

workingPath = tempfile.mkdtemp()
# Copy the profile into the temporary path
os.makedirs(os.path.join(workingPath, libraryPath)
shutil.copy(arguments.profile, os.path.join(workingPath, libraryPath))

# Place the script into the outset folder in the temporary path
os.makedirs(os.path.join(workingPath, libraryPath, outsetPath))
# This is the base profile installer script
script='''#!/bin/sh
if [[ $USER == "%s" ]]; then
    /usr/bin/profiles -IvF "/Library/Profiles/%s"
fi''' % (arguments.name, os.path.basename(arguments.profile))
# write script to file in temp directory
with open(os.path.join(workingPath, libraryPath, outsetPath, 'profile-%s.sh' % arguments.name), 'wb') as outsetScript:
    outsetScript.write(script)
    
# Call productbuild to create a package out of the temp folder
cmd = ['/usr/bin/productbuild', '--content', workingPath, '--identifier', arguments.identifier, arguments.output]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(pbout, pberr) = proc.communicate()

if pberr:
    print "Error: %s" % pberr
print pbout