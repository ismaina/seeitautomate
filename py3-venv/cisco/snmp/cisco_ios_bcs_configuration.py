#!/usr/bin/env python
#Author is Maina Wanjau Copyright @Maina Wanjau

from __future__ import print_function
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
import sys
import time
import select
import socket
import paramiko
import netmiko
import re
import csv
ssh_exceptions = (netmiko.ssh_exception.NetMikoAuthenticationException,
                  netmiko.ssh_exception.NetMikoTimeoutException, netmiko.NetMikoTimeoutException,
                  netmiko.NetMikoAuthenticationException, netmiko.NetmikoTimeoutError, netmiko.NetmikoAuthError,
                  netmiko.ssh_exception.SSHException, netmiko.ssh_exception.AuthenticationException,
                  paramiko.OPEN_FAILED_CONNECT_FAILED, socket.timeout, paramiko.SSHException)
class SeeItAtutomate:

    def __init__(self):
        #initialize general configs
        self.connection = ConnectHandler
        self.login = ''
        self.date_time = datetime
        self.config_end_time = datetime
        self.script_time = datetime
        self.script_end_time = datetime
        self.Node_Name = ''   
        self.IP_Address = '' 
        self.Region = 'Region'  
        self.Vendor = 'Vendor'  
        self.Primary_Engineer = 'Primary_Engineer'    
        self.Aggregation_Point = 'Aggregation_Point'   
        self.filepath = 'filepath'   
        self.CARRIER_TRANSMISSION = 'CARRIER_TRANSMISSION'
        self.user = ''
        self.pw = ''
        self.tm = ''
        self.config_set = []
        self.failed_ips = []
        #start by getting user details the user
        self.Credentials() #user to enter credentials
        self.ssh_exceptions = ssh_exceptions

    def Credentials(self): #get user credentials
        self.user=input('Enter username: ')
        self.pw = getpass() #encrypted password from getpass() class
        #self.Authenticate(self.user,self.pw)
        self.readExcel(self.user,self.pw)

    def readExcel(self, cred_uname, cred_pw):
        config_file = open("bcs_snmp_config.txt")
        config_set = config_file.read()
        self.config_set = config_set
        
        with open('Cisco_IOS_BCS_portal.csv') as ip_add_f: # a simple list of IP addresses you want to connect to each one on a new line 
            #reader = csv.reader(ip_add_f)
            reader = csv.DictReader(ip_add_f)
            start_time = self.date_time.now()    #begining of script time
            for row in reader:
                self.IP_Address = str(row['IP_Address'])
                self.Node_Name = row['Node_Name']
                self.Vendor = str(row['Vendor']).lower()
                #Attempt to login to device and put commands
                try:   
                    print('Attempting to login to ',self.Node_Name)       
                    self.NetmAuthenticate(cred_uname,cred_pw,self.IP_Address,self.Vendor) 
                except:  #if failed to login log the devices that failed
                    print("failed to login to ", self.Node_Name)
                    self.failed_ips.append(self.IP_Address)
            end_time = self.date_time.now()
            print('Total time spent is : ', end_time-start_time)
        config_file.close()
        ip_add_f.close() #closed the opened excel session
        if len(self.failed_ips) == 0:
            print(" All devices were successful")
        else:
            self.failed_ips_print()
    def NetmAuthenticate(self,nt_user,nt_pw,nt_IP_Address,nt_Vendor):
        #print('... Reading device info...')
        
        my_device = {
            'host': nt_IP_Address,
            'username': nt_user,
            'password': nt_pw,
            'device_type': nt_Vendor,
        }

        if my_device['device_type'] in 'cisco_ios': #Execute Huawei Commands
            #print('...Authenticating...')
            try:
                #print('... Attempting Netmiko Auth...')
                login = ConnectHandler(**my_device)
                output = ''
                start_time = self.date_time.now()    #begining of script time
                if nt_pw: #if authenticated then push commands
                    print('Successfully Logged in')
                    #output = login.send_command('show version | i time')
                    output = login.send_config_set(self.config_set)
                    print("\n\n>>>>>>>>> Begin of Output for {0} <<<<<<<<<\n".format(nt_IP_Address))
                    print(output)
                    login.disconnect()
                    print("\n\n>>>>>>>>> End of Output for {0} <<<<<<<<<\n".format(nt_IP_Address))
                else: #if not authenticated return error
                    print('>>>>>>>>>__Huawei Authentication failure??<<<<<<<<')    
            except self.ssh_exceptions as error:
                print('Authentication Error', error)
            except:
                print('Unknown Error')

        else:       #doesnt recognize platform
            print('Doesnt recognise Platform\a')

    def CiscoCommands(self):
        result = self.connection.find_prompt()
        result += self.connection.send_command('show users')
        print(result)
    def failed_ips_print(self):
        print(" The following devices failed to be logged in")
        print("***___________________________**")
        for ip in self.failed_ips:
            print(ip)
        print("***___________________________**")
         
    def CloseConnection(self):
        print(">>>>>>>>> End of Output <<<<<<<<<")
        result = self.connection.disconnect()
        print('You have been disconnected')
        
a = SeeItAtutomate()  
