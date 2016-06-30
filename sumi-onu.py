#### This is my first actual project, I will try to develop a script to facilitate
#### our job during Spectrum analysis, specifically when observing Sumitomo ONUs.

# Importing libraries that we will need
import time
import paramiko
import re
import sys
import os
import glob
import getpass

# define a function to open ssh connection
def open_ssh_conn(hostname, cred_file, usern, passw):
    try:
        credentials = open(cred_file, 'r')
        credentials.seek(0)
        #usern = credentials.readline()

        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname, username = usern, password = passw)
        connection = session.invoke_shell()

        onu = raw_input("Give me the ONU number and don\'t worry about the chassis number: ")
        connection.send("set cli pagination off\n")
        connection.send("show runn epononu 1/" + onu + "\n")
        connection.send("show onu uniport 1/" + onu + "\n")
        time.sleep(1)

        cpr_output = connection.recv(65535)

        if re.search(r"% does not exist", cpr_output):
            print "That is not a valid ONU number for %s" % hostname
        else:
            print "DONE"

        print cpr_output + "\n"

        session.close()

    except paramiko.AuthenticationException:
        print "Something went wrong during authentication, check username and password"
        get_usern()
        get_passw()
        
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

def get_usern():
    usern = raw_input("Give me username (we will only need this once): ")
    return usern
usern = get_usern()

def get_passw():
    passw = getpass.getpass()
    return passw
passw = get_passw()

while True:
    hostname = raw_input("Give me the hostname or IP: ")
    credentials_file = "credentials_file"
    open_ssh_conn(hostname, credentials_file, usern, passw)
