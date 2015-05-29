#Outset Dock Profiler

This script creates a package to use with [Outset](https://github.com/chilcote/outset) that will install a user-level profile for a specific user of your choice.

Provide a username and a profile, and a script will be placed in the `login-every` (or `login-once` if you specify) directory that will check if the current username is the one you provide, and then attempt to install a user-level profile.

*NOTE: This script does ***not*** check to see if your profile is User or System.  If you provide a System-level profile, it'll still apply to every user regardless once installed. Check your profile before using it.*

##Usage

```
$ ./dock_profiler.py -h
usage: dock_profiler.py [-h] -p PROFILE -n NAME [-i IDENTIFIER] [-o OUTPUT]
                        [--once] [-s IDENTITY]

Creates a package for Outset that will install a profile for a specific user
on login.

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        path to profile to load. Required
  -n NAME, --name NAME  name of user to trigger on login. Required
  -i IDENTIFIER, --identifier IDENTIFIER
                        identifier of package, defaults to
                        "com.organization.profile"
  -o OUTPUT, --output OUTPUT
                        path to output package, defaults to "Outset-
                        Profile.pkg"
  --once                load profile once, not every login
  -s IDENTITY, --sign IDENTITY
                        sign package with valid identity
```

The required arguments are `--profile` (path to a profile) and `--name` (the name of the user to trigger the profile installation).

`--identifier` can be specified to create an identifier for the package (and the package receipt).  

`--output` can be specified for an output path.

`--once` can be specified to place the profile in `login-once` instead of `login-every`.  This will cause the profile only to be installed the next time the user logs in, and then it won't try again in the future.

`--sign IDENTITY` will sign the resulting package with a valid identity.  Use `/usr/bin/security find-identity -p basic` to list possible identities you can use to sign the package with.

## Example

```
./dock_profiler.py -p DockStudent.mobileconfig -n student -i org.sacredsf.profile.dock.student -o Outset-Dock-Student.pkg --sign "Developer ID Installer"

productbuild: Using timestamp authority for signature
productbuild: Signing product with identity "Developer ID Installer" from keychain /Users/nmcspadden/Library/Keychains/login.keychain
productbuild: Adding certificate "Developer ID Certification Authority"
productbuild: Adding certificate "Apple Root CA"
productbuild: Wrote product to Outset-Dock-Student.pkg
```

This will create the "Outset-Dock-Student.pkg" file that will install a profile into `/Library/Profiles/DockStudent.mobileconfig`, and a script into `/usr/local/outset/login-every/profile-student.sh`. 