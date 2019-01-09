#!/usr/bin/env python
#Author is Maina Wanjau Copyright @Maina Wanjau

from __future__ import print_function
from getpass import getpass
from datetime import datetime
from napalm import get_network_driver
from getpass import getpass
import sys
import json
import re
import csv
import json

class SeeitAutomate():
    def __init__(self):
        self.driver = ''
        self.username = ''
        self.password = ''
        self.ip_address = ''
        self.node_name =  ''
        self.date_time = datetime
        self.config_end_time = datetime
        self.script_time = datetime
        self.script_end_time = datetime
        self.ios_image = ''
        self.vendor = ''
        self.csv_path = ''

    #get user credentials
    def get_credentials(self):
        self.username = str(input('Enter your tacacs username: ')).lower()
        self.password = getpass()
        self.read_one_device()
        #self.read_excel()
    
    def read_one_device(self):
        self.ip_address = str(input('Enter ip address: '))
        print('Enter device version*\n cisco_ios or huawei')
        self.vendor = str(input('vendor ')).lower()
        self.netpalm_authentication(self.ip_address,self.vendor)

    def read_excel(self):
        with open('Enterprise_Access_Switch_Descriptions.csv') as csv_file:
            reader = csv.DictReader(csv_file) #read the specified excel
            start_time = self.date_time.now() #log start time of the script
            for row in reader:
                self.ip_address = str(row['IP_Address']) #get the Ip address on this Column
                self.node_name = str(row['Node_Name'])
                self.vendor = str(row['Vendor']).lower()
                try:
                    print('Attempting to login to '+ self.node_name)
                    self.netpalm_authentication(self.ip_address,self.vendor)
                except:
                    print("\n Failed to login to "+self.node_name)
            end_time = self.date_time.now()
            print('Total time spent is ',end_time-start_time)

    def netpalm_authentication(self):
        print(" ...... Reading device info for",self.node_name,"........")
        my_device ={
            'hostname'  :   self.ip_address,
            'username'  :   self.username,
            'password'  :   self.password
        }
        try:
            output = ''
            if self.password:
                print("Successfully logged in to ",self.node_name)
                if self.vendor in 'huawei':
                    vendor = 'ce'
                    self.driver = get_network_driver(vendor)
                    vrrp = self.driver(**my_device)
                    vrrp.open()
                    output = vrrp.get_facts()
                    print("\n\n>>>>>>>>>>> Begin output {0} <<<<<<<<<<<<<<\n")
                    print(json.dumps(output, indent=4))
                    print("\n\n>>>>>>>>>>> End output {0} <<<<<<<<<<<<<<\n")
                    vrrp.close()
                elif self.vendor in 'cisco_ios':
                    vendor='ios'
                    self.driver = get_network_driver('ios')
                    cisco = self.driver(**my_device)
                    cisco.open()
                    output = cisco.get_facts()
                    print("\n\n>>>>>>>>>>> Begin output {0} <<<<<<<<<<<<<<\n")
                    print(json.dumps(output, indent=4))
                    print("\n\n>>>>>>>>>>> End output {0} <<<<<<<<<<<<<<\n")
                    cisco.close()
                else:
                    print("_________ Doesnt Recognize Platform ___________")
                print("You have been disconnected")
            else:
                print("\n>>>>>>>>>>>>>______Authentication Failure_____<<<<<<<<<<")
        except:
            print('Unknown Error')
a = SeeitAutomate()
a.get_credentials()