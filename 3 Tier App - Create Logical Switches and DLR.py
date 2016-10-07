#!/usr/bin/env python

"""
Python script created by Caio Oliveira - oliveirac@vmware.com
This script creates 3 NSX Logical Switches and 1 NSX Distributed Logical Router with no Control-VM
This script is an excellent tool to use with 3-Tier-App or to demonstrate how simple is to create 3xLS and 1xDLR in NSX
"""

# DONT CHANGE - START 
import requests
from xml.etree import ElementTree
requests.packages.urllib3.disable_warnings()
headers = {'Content-Type': 'application/xml'}
# DONT CHANGE - FINISH 

# ENVIRONMENT VARIABLES - YOU CAN CHANGE 
nsxmanager = '192.168.1.190' # IP or FQDN
admin = 'admin' # NSX Manager - admin login 
password = 'VMware1!' # NSX Manager - admin password
transportZoneName = 'TZ' # Transport-Zone should be already created
webGW = '172.16.10.1' # Default Gateway for Logical Switch Web Tier
appGW = '172.16.20.1' # Default Gateway for Logical Switch App Tier
dbGW = '172.16.30.1' # Default Gateway for Logical Switch DB Tier
nameDLR = 'DLR-3-Tier-App' # Name of the Distributed Logical Router - MUST BE UNIQUE

# DONT CHANGE NOTHING BELOW

# TRANSPORT ZONE 
# Get Transport Zone ID with Transport Zone Name
transportZone = ''
responseTZ = requests.get('https://'+nsxmanager+'/api/2.0/vdn/scopes', verify=False, auth=(admin, password), stream=True)
treeTZ = ElementTree.parse(responseTZ.raw)
for vdnScope in treeTZ.iter('vdnScope'):
	if vdnScope.find('name').text == transportZoneName:
		transportZone = vdnScope.find('objectId').text
#print transportZone

# WEB TIER
# XML for Logical Switch Web Tier 
xml_data_LSWeb = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <virtualWireCreateSpec>
        <name>Web Tier</name>
        <description>Web Tier for 3-Tier App</description>
        <tenantId></tenantId>
        <controlPlaneMode>UNICAST_MODE</controlPlaneMode>
        <guestVlanAllowed>false</guestVlanAllowed>
</virtualWireCreateSpec>
"""
# Creation of Logical Switch Web 
print "Creating Logical Switch Web Tier."
responseLSWeb = requests.post('https://'+nsxmanager+'/api/2.0/vdn/scopes/'+transportZone+'/virtualwires', verify=False, auth=(admin, password), data=xml_data_LSWeb, headers=headers)
LSWeb = responseLSWeb.text
if responseLSWeb.status_code == 201:
    print "Logical Switch Web Tier created!"

# APP TIER
# XML for Logical Switch App Tier 
xml_data_LSApp = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <virtualWireCreateSpec>
        <name>App Tier</name>
        <description>App Tier for 3-Tier App</description>
        <tenantId></tenantId>
        <controlPlaneMode>UNICAST_MODE</controlPlaneMode>
        <guestVlanAllowed>false</guestVlanAllowed>
</virtualWireCreateSpec>
"""
# Creation of Logical Switch App 
print "Creating Logical Switch App Tier."
responseLSApp = requests.post('https://'+nsxmanager+'/api/2.0/vdn/scopes/'+transportZone+'/virtualwires', verify=False, auth=(admin, password), data=xml_data_LSApp, headers=headers)
LSApp = responseLSApp.text
if responseLSApp.status_code == 201:
    print "Logical Switch App Tier created!"

# DB TIER
# XML for Logical Switch DB Tier 
xml_data_LSDB = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <virtualWireCreateSpec>
        <name>DB Tier</name>
        <description>DB Tier for 3-Tier App</description>
        <tenantId></tenantId>
        <controlPlaneMode>UNICAST_MODE</controlPlaneMode>
        <guestVlanAllowed>false</guestVlanAllowed>
</virtualWireCreateSpec>
"""
# Creation of Logical Switch DB 
print "Creating Logical Switch DB Tier."
responseLSDB = requests.post('https://'+nsxmanager+'/api/2.0/vdn/scopes/'+transportZone+'/virtualwires', verify=False, auth=(admin, password), data=xml_data_LSDB, headers=headers)
LSDB = responseLSDB.text
if responseLSDB.status_code == 201:
    print "Logical Switch DB Tier created!"

# Discover Data
response = requests.get('https://'+nsxmanager+'/api/2.0/vdn/virtualwires/'+LSWeb, verify=False, auth=(admin, password), stream=True)
tree = ElementTree.parse(response.raw)
#webDVSPortGroup = tree.find("vdsContextWithBacking/switch/objectId").text
#webDVSPortGroupName = tree.find("vdsContextWithBacking/switch/objectTypeName").text
datacenterMoid = tree.find("vdsContextWithBacking/switch/scope/id").text
datacenterName = tree.find("vdsContextWithBacking/switch/scope/name").text

# DLR
# XML for DLR 
xml_data_DLR = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<edge>
	<datacenterMoid>"""+datacenterMoid+"""</datacenterMoid>
	<datacenterName>"""+datacenterName+"""</datacenterName>
	<tenant>default</tenant>
	<name>"""+nameDLR+"""</name>
	<enableAesni>false</enableAesni>
	<enableFips>false</enableFips>
	<vseLogLevel>emergency</vseLogLevel>
	    <autoConfiguration>
        <enabled>true</enabled>
        <rulePriority>high</rulePriority>
    </autoConfiguration>
    <type>distributedRouter</type>
    <isUniversal>false</isUniversal>
	<interfaces>
		<interface>
			<label>WEB</label>
			<name>WEB</name>
			<addressGroups>
				<addressGroup>
				    <primaryAddress>"""+webGW+"""</primaryAddress>
				    <subnetMask>255.255.255.0</subnetMask>
				    <subnetPrefixLength>24</subnetPrefixLength>
				</addressGroup>
			</addressGroups>
			<mtu>1500</mtu>
			<type>internal</type>
			<isSharedNetwork>false</isSharedNetwork>
			<isConnected>true</isConnected>
			<connectedToId>"""+LSWeb+"""</connectedToId>
			<connectedToName>Web Tier</connectedToName>
		</interface>
        <interface>
            <label>APP</label>
            <name>APP</name>
            <addressGroups>
                <addressGroup>
                    <primaryAddress>"""+appGW+"""</primaryAddress>
                    <subnetMask>255.255.255.0</subnetMask>
                    <subnetPrefixLength>24</subnetPrefixLength>
                </addressGroup>
            </addressGroups>
            <mtu>1500</mtu>
            <type>internal</type>
            <isSharedNetwork>false</isSharedNetwork>
            <isConnected>true</isConnected>
            <connectedToId>"""+LSApp+"""</connectedToId>
            <connectedToName>App Tier</connectedToName>
        </interface>
        <interface>
            <label>DB</label>
            <name>DB</name>
            <addressGroups>
                <addressGroup>
                    <primaryAddress>"""+dbGW+"""</primaryAddress>
                    <subnetMask>255.255.255.0</subnetMask>
                    <subnetPrefixLength>24</subnetPrefixLength>
                </addressGroup>
            </addressGroups>
            <mtu>1500</mtu>
            <type>internal</type>
            <isSharedNetwork>false</isSharedNetwork>
            <isConnected>true</isConnected>
            <connectedToId>"""+LSDB+"""</connectedToId>
            <connectedToName>DB Tier</connectedToName>
        </interface>
    </interfaces>
    <appliances>
        <deployAppliances>false</deployAppliances>
    </appliances>
    <features>
        <firewall>
            <version>1</version>
            <enabled>true</enabled>
            <globalConfig>
                <tcpPickOngoingConnections>false</tcpPickOngoingConnections>
                <tcpAllowOutOfWindowPackets>false</tcpAllowOutOfWindowPackets>
                <tcpSendResetForClosedVsePorts>true</tcpSendResetForClosedVsePorts>
                <dropInvalidTraffic>true</dropInvalidTraffic>
                <logInvalidTraffic>false</logInvalidTraffic>
                <tcpTimeoutOpen>30</tcpTimeoutOpen>
                <tcpTimeoutEstablished>3600</tcpTimeoutEstablished>
                <tcpTimeoutClose>30</tcpTimeoutClose>
                <udpTimeout>60</udpTimeout>
                <icmpTimeout>10</icmpTimeout>
                <icmp6Timeout>10</icmp6Timeout>
                <ipGenericTimeout>120</ipGenericTimeout>
            </globalConfig>
            <defaultPolicy>
                <action>deny</action>
                <loggingEnabled>false</loggingEnabled>
            </defaultPolicy>
            <firewallRules>
                <firewallRule>
                    <id>131074</id>
                    <ruleTag>131074</ruleTag>
                    <name>firewall</name>
                    <ruleType>internal_high</ruleType>
                    <enabled>true</enabled>
                    <loggingEnabled>false</loggingEnabled>
                    <description>firewall</description>
                    <action>accept</action>
                    <source>
                        <exclude>false</exclude>
                        <vnicGroupId>vse</vnicGroupId>
                    </source>
                </firewallRule>
                <firewallRule>
                    <id>131073</id>
                    <ruleTag>131073</ruleTag>
                    <name>default rule for ingress traffic</name>
                    <ruleType>default_policy</ruleType>
                    <enabled>true</enabled>
                    <loggingEnabled>false</loggingEnabled>
                    <description>default rule for ingress traffic</description>
                    <action>deny</action>
                </firewallRule>
            </firewallRules>
        </firewall>
    </features>
    <cliSettings>
        <remoteAccess>true</remoteAccess>
        <userName>admin</userName>
        <password>VMware1!VMware1!</password>
    </cliSettings>
    <hypervisorAssist>false</hypervisorAssist>
    <queryDaemon>
        <enabled>false</enabled>
        <port>5666</port>
    </queryDaemon>
</edge>
"""
#print xml_data_DLR
# Creation of DLR 
print "Creating DLR"
responseDLR = requests.post('https://'+nsxmanager+'/api/4.0/edges', verify=False, auth=(admin, password), data=xml_data_DLR, headers=headers)
if responseDLR.status_code == 201:
    print "Distributed Logical Router created!"

