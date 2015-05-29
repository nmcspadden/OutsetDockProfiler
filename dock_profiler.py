#!/usr/bin/python

import argparse
import os
import shutil
import tempfile
import subprocess

p = argparse.ArgumentParser(description="Creates a package for Outset that will install a profile for a specific user on login.")
p.add_argument("-p","--profile", help='path to profile to load. Required', required=True)
p.add_argument("-n","--name", help='name of user to trigger on login. Required', required=True)
p.add_argument("-i","--identifier", help='identifier of package, defaults to "com.organization.profile"', default='com.organization.profile')
p.add_argument("-o","--output", help='path to output package, defaults to "Outset-Profile.pkg"', default='Outset-Profile.pkg')
p.add_argument('--once', help='load profile once, not every login',action='store_true')
p.add_argument("-s","--sign", help='sign package with valid identity',metavar='IDENTITY')
arguments = p.parse_args()

libraryPath = 'Library/Profiles'
outsetPath = 'usr/local/outset/login-every'
if (arguments.once):
    outsetPath = 'usr/local/outset/login-once'

workingPath = tempfile.mkdtemp()
# Copy the profile into the temporary path
os.makedirs(os.path.join(workingPath, libraryPath))
shutil.copy(arguments.profile, os.path.join(workingPath, libraryPath))

# Place the script into the outset folder in the temporary path
os.makedirs(os.path.join(workingPath, outsetPath))
# This is the base profile installer script
script='''#!/bin/sh
if [[ $USER == "%s" ]]; then
    /usr/bin/profiles -IvF "/Library/Profiles/%s"
fi
''' % (arguments.name, os.path.basename(arguments.profile))
# write script to file in temp directory
with open(os.path.join(workingPath, outsetPath, 'profile-%s.sh' % arguments.name), 'wb') as outsetScript:
    outsetScript.write(script)
os.chmod(os.path.join(workingPath, outsetPath, 'profile-%s.sh' % arguments.name), 0755)
# Call productbuild to create a package out of the temp folder
cmd = ['/usr/bin/productbuild', '--content', workingPath, '--identifier', arguments.identifier, arguments.output]
if arguments.sign:
    cmd += ['--sign', arguments.sign]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(pbout, pberr) = proc.communicate()

if pberr:
    print "Error: %s" % pberr
print pbout