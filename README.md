###RHN-UTILS
Author: Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
Description: Those scripts are used for providing some interaction with RHN/Satellite  API to ease system management on them.

Typical structure is .py with the python code and .sh to ease the input of values

Feel free to send any comment or patch to improve them, but keep in mind
that are just basic scripts to demonstrate some of the capabilities of the
software.

rhn-common has the values for userid/password to interact with API and
gathers satellite hostname to pass it automatically to python scripts

Scripts are prepared to be executed from /root/scripts/ but you can tweak
rhn-common to set a new path.

