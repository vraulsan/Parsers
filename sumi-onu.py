#### This is my first project, I will try to develop a script to facilitate
#### our job during Spectrum analysis, specifically when observing Sumitomo ONUs.

# Importing libraries that we will might need
import time
import paramiko
import re
import sys
import os
import glob
import getpass

# define a function to open ssh connection
# this is a function with 3 arguments, right now we are not utilizing cred_file though, that will come later
def open_ssh_conn(hostname, cred_file, usern, passw):
    try:
        # will open file with credentials, again, we will use this later in another version
        credentials = open(cred_file, 'r')
        credentials.seek(0)
        #usern = credentials.readline()
        
        # establish session and pass to variable called session
        session = paramiko.SSHClient()
        # auto-accept unknown_hosts 
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # pass credentials to connect function
        session.connect(hostname, username = usern, password = passw)
        # this is a dynamic connection to the host
        connection = session.invoke_shell()
        
        # we'll ask the user for an ONU number and assign to variable onu
        onu = raw_input("Give me the ONU number and don\'t worry about the chassis number: ")
        # send these commands to the device
        connection.send("set cli pagination off\n")
        connection.send("show runn epononu 1/" + onu + "\n")
        connection.send("show onu uniport 1/" + onu + "\n")
        time.sleep(1)
        
        # take the output from the device and pass it to variable cpr_output
        cpr_output = connection.recv(65535)
        
        # if the output contains "does not exist", tell the user that the ONU number is invalid
        if re.search(r"% does not exist", cpr_output):
            print "That is not a valid ONU number for %s" % hostname
        else:
            print "DONE"
        
        # here we print the device output to the screen
        print cpr_output + "\n"
        
        # and we close the session
        session.close()

    # here the first exception will be if paramiko finds an authentication error, let user know
    except paramiko.AuthenticationException:
        print "Something went wrong during authentication, check username and password"
        # we prompt the user to enter the username and passw one more time
        get_usern()
        get_passw()
    # if for other reason connection can't establish, that means the device is not there (wrong hostname/IP)
    # this will repeat until we get a valid hostname/IP
    except:
        print "Cant find that Sumi Chassis, try again."

print "####################################################################"
print "#                                                                  #"
print "#              SHOW ME THE SUMITOMO ONU Ver 1.0 beta               #"
print "#                 (useful when doing Spectrum)                     #"
print "#                                                                  #"
print "#                  Developed by Victor Sanchez                     #"
print "#                                                                  #"
print "#                        for BHN ATS Team                          #"
print "#                                                                  #"
print "#            Press CTRL-C at any time to stop the script           #"
print "####################################################################"

# define function to get username
def get_usern():
    usern = raw_input("Give me username (we will only need this once): ")
    return usern
    
# step 1. we call the usern function
usern = get_usern()

# define function to get password
def get_passw():
    passw = getpass.getpass()
    return passw
    
# step 2. we call the passw function
passw = get_passw()

# step 3. forever will call open_ssh_conn function, using the same usern and passw provided in step 1 and 2
while True:
    hostname = raw_input("Give me the hostname or IP: ")
    credentials_file = "credentials_file"
    open_ssh_conn(hostname, credentials_file, usern, passw)
