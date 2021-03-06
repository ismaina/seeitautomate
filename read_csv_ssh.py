#!/usr/bin/env python
#Author is Maina Wanjau Copyright @Maina Wanjau

from __future__ import print_function
from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import sys
import time
import select
import paramiko
import re
import csv

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
        self.IOS_Image = ''   
        self.IOS_Version = ''
        self.Description = ''
        self.Region = 'Region'  
        self.Vendor = 'Vendor'  
        self.Primary_Engineer = 'Primary_Engineer'    
        self.Aggregation_Point = 'Aggregation_Point'   
        self.filepath = 'filepath'   
        self.CARRIER_TRANSMISSION = 'CARRIER_TRANSMISSION'
        self.user = ''
        self.pw = ''
        self.tm = ''
        #start by getting user details the user
        self.Credentials() #user to enter credentials

    def Credentials(self): #get user credentials
        self.user=input('Enter username: ')
        self.pw = getpass() #encrypted password from getpass() class
        #self.Authenticate(self.user,self.pw)
        self.readExcel(self.user,self.pw)

    def readExcel(self, cred_uname, cred_pw):
        with open('Enterprise_Access_Switch_Descriptions.csv') as ip_add_f: # a simple list of IP addresses you want to connect to each one on a new line 
            #reader = csv.reader(ip_add_f)
            reader = csv.DictReader(ip_add_f)
            start_time = self.date_time.now()    #begining of script time
            for row in reader:
                self.IP_Address = str(row['IP_Address'])
                self.Node_Name = row['Node_Name']
                self.Vendor = str(row['Vendor']).lower()
                #print(self.Vendor)

                try:   #Attempt to login to device and put commands
                    print('Attempting to login to ',self.Node_Name)
                    self.NetmAuthenticate(cred_uname,cred_pw,self.IP_Address,self.Vendor)
                    
                except:  #if failed to login log the devices that failed
                    print("failed to login to ", self.Node_Name)
                #self.IP_Address = row['Area_address']
                #self.Description = row['Description']
                #self.IP_Address = row[0]
                #self.Credentials(self.IP_Address)
                #print(self.Node_Name,self.IP_Address,self.Vendor)
            end_time = self.date_time.now()
            print('Total time spent is : ', end_time-start_time)

        ip_add_f.close() #closed the opened excel session
         
    
    def NetmAuthenticate(self,nt_user,nt_pw,nt_IP_Address,nt_Vendor):
        #print('... Reading device info...')
        
        my_device = {
            'host': nt_IP_Address,
            'username': nt_user,
            'password': nt_pw,
            'device_type': nt_Vendor,
        }
        
        if my_device['device_type'] in 'huawei': #Execute Huawei Commands
            #print('...Authenticating...')
            try:
                #print('... Attempting Netmiko Auth...')
                login = ConnectHandler(**my_device)
                output = ''
                if nt_pw: #if authenticated then push commands
                    print('Successfully Logged in')
                    output = login.send_command('display version | i : uptime')
                    print("\n\n>>>>>>>>> Begin of Output {0} <<<<<<<<<\n")
                    print(output)
                    login.disconnect()
                    print("\n\n>>>>>>>>> End of Output {0} <<<<<<<<<\n")
                else: #if not authenticated return error
                    print('>>>>>>>>>__Huawei Authentication failure??<<<<<<<<')
                #print(output)
                print('Disconnecting....')
                print('You have been disconnected\n')
                #self.CloseConnection()      
            except NetMikoAuthenticationException:
                print('Authentication Error') 
            except:
                print('Unknown Error')

            print(self.IP_Address,' is a Huawei Device')

        elif my_device['device_type'] in 'cisco_ios': #Execute Huawei Commands
            #print('...Authenticating...')
            try:
                #print('... Attempting Netmiko Auth...')
                login = ConnectHandler(**my_device)
                output = ''
                start_time = self.date_time.now()    #begining of script time
                if nt_pw: #if authenticated then push commands
                    print('Successfully Logged in')
                    output = login.send_command('show version | i time')
                    print("\n\n>>>>>>>>> Begin of Output {0} <<<<<<<<<\n")
                    print(output)
                    login.disconnect()
                    print("\n\n>>>>>>>>> End of Output {0} <<<<<<<<<\n")
                else: #if not authenticated return error
                    print('>>>>>>>>>__Huawei Authentication failure??<<<<<<<<')    
            except NetMikoAuthenticationException:
                print('Authentication Error')
            except:
                print('Unknown Error')

        else:       #doesnt recognize platform
            print('Doesnt recognise Platform\a')
    def HuaweiCommands(self):
        #elf.date_time.now()
        config_set = ['screen-length 0 temporary','screen-length 0 temporary']
        #result = self.connection.send_command('screen-length 0 temporary')
        #result += self.connection.send_command('display users')
        #print(result)
        #print(config_set)

    def CiscoCommands(self):
        date_time = datetime.now()
        result = self.connection.find_prompt()
        result += self.connection.send_command('show users')
        print(result)

    def CloseConnection(self):
        print(">>>>>>>>> End of Output <<<<<<<<<")
        result = self.connection.disconnect()
        print('You have been disconnected')
        
a = SeeItAtutomate()  
