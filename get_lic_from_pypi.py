import requests
import pandas as pd
import simplejson
import pip

def get_lic(package_with_version): # pass the package name in format bs4==0.0.1
    # split the package name and extract [0] i.e. name of the package
    package = str(package_with_version).split("==")
    #print package[0] # print to see if we get what we expect

    # URL to GET the package license from
    url = "https://pypi.python.org/pypi/{}/json".format(package[0])
    lic = requests.get(url)
    if lic.status_code != requests.codes.ok: # for internal packages we get 404
        return [package[0], None, None]
    lic = lic.json()
    #print "Package:" + package[0] + ", License type:->" + lic['info']['license'] + "<-" + lic['info']['summary']
    # if not lic['info']['license'] == 'UNKNOWN' or len(lic['info']['license']) == 0:
        #print "Lic type unknown"
    # if 'License' in lic['info']['classifiers']:
    #     print lic['info']['classifiers']
    return [package[0], lic['info']['license'], lic['info']['summary']]

# query pip and get installed packages list and sort them
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
    for i in installed_packages])

# extract each list from installed packages list and pass it to get_lic function to GET license
pkg_lic_info = [get_lic(x) for x in installed_packages_list]

#print pkg_lic_info

pd_packages = pd.DataFrame(pkg_lic_info, columns=['Package_Name','License_Type','Description'])

print pd_packages
#
pd_packages.to_csv('pd_packages.csv')

remove_unknown_lic = pd_packages["License_Type"].str.contains("UNKNOWN")
pd_packages["UNKNOWN"] = remove_unknown_lic

print pd_packages
