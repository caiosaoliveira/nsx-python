#!/usr/bin/env python

"""
Python script created by Caio Oliveira - oliveirac@vmware.com
This script was used during API session in Delta Force Brazil 2016 and Delta Force NOLA 2016
This script displays all Logical Switches in NSX-v and after that create a new Logical Switch
"""

import requests
from xml.etree import ElementTree
requests.packages.urllib3.disable_warnings()
headers = {'Content-Type': 'application/xml'}

print ""
print "### DELTA FORCE NSX ###"
print ""

# GET LOGICAL SWITCHES
response = requests.get('https://192.168.1.190/api/2.0/vdn/scopes/vdnscope-1/virtualwires', verify=False, auth=('admin', 'VMware1!'), stream=True)
tree = ElementTree.parse(response.raw)
for virtualWire in tree.iter('virtualWire'):
    print 'Switch Name: ' + virtualWire.find('name').text
    print 'Switch ID: ' + virtualWire.find('objectId').text

# CREATE A LOGICAL SWITCH
xml_data = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <virtualWireCreateSpec>
        <name>Delta Force NSX - Python</name>
        <description>Creating Logical Switch with Python</description>
        <tenantId></tenantId>
	</virtualWireCreateSpec>
"""
print ""
print "Adding a Logical Switch to NSX."
response = requests.post('https://192.168.1.190/api/2.0/vdn/scopes/vdnscope-1/virtualwires', verify=False, auth=('admin', 'VMware1!'), data=xml_data, headers=headers)

if response.status_code == 201:
	print "Logical Switch (ID=%s) Created" % response.text
else:
	print "Logical Switch Not Created"

print ""
print "### DELTA FORCE NSX ###"
print ""



