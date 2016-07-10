import MySQLdb
import re
import time
import paramiko
import sys
import os
import glob
import getpass
import platform, os, subprocess
import log

###########################################################
def check_input(mini, maxi, msg):
    while True:
            try:
                vari = int(raw_input(msg))
            except ValueError:
                continue
            else:
                if vari < mini or vari > maxi:
                    continue
                else:
                    break
    return vari

######### define database class ###############
class Database:
    # read the lines of a file called dbconfig.txt which holds the database information
    dbfile = open("dbconfig.txt")
    host = dbfile.readline()[0:-1] # avoid reading the \n at the end of each line of dbconfig.txt
    user = dbfile.readline()[0:-1]
    passwd = dbfile.readline()[0:-1]
    db = dbfile.readline()[0:-1]
    def __init__(self):
        self.connection = MySQLdb.connect(host = self.host,
                                            user = self.user,
                                            passwd = self.passwd,
                                            db = self.db)
    def query(self, q):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        return cursor.fetchall()

    def queryone(self, q):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        return cursor.fetchone()
    def __del__(self):
        self.connection.close()
if __name__ == "__main__":
    db = Database()
################################################

################# searching function #######################
def search_func():
    msg = """
What do you want to search by:
    \t1. Search by Name
    \t2. Search by Address
    \t3. Search by City
    \t4. Search by Vendor

Enter the number you want to search by: """
    bywhat = check_input(1, 4, msg)

    if bywhat == 1:
        bywhat = "Name"
    elif bywhat == 2:
        bywhat = "Address"
    elif bywhat == 3:
        bywhat = "City"
    elif bywhat == 4:
        bywhat = "Vendor"

    what = raw_input("Search by %s: " % bywhat)
    q = ("SELECT * FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))
    qIP = ("SELECT `Mgmt IP` FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))

    search = db.query(str(q))
    e = 0
    for entry in search:
            print "----------------------------------------------------"
            e += 1
            print "%d. " % e,
            print "%s" % entry['Name'],
            print "\n\tAddress: %s" % entry['Address'], 
            print "\n\tVendor: %s" % entry['Vendor'],
            print "\n\tCity: %s" % entry['City'],
            print "\n\tMgmt IP: %s" % entry['Mgmt IP'],
            status = subprocess.call(
                ['ping', '-c1', '-W10', '-w1', entry['Mgmt IP']],
                stdout = open(os.devnull, 'wb'))
            if status == 0:
                print "is", 
                log.infog("UP")
            else:
                print "is",
                log.err("DOWN")
            print "----------------------------------------------------"
    search_IP = list(db.query(str(qIP)))
    return search_IP
################################################################
def the_IP(search_IP):
    msg = "If you would like to get an output from the box, enter the number for that box now.\nOtherwise, enter 0 to search again: "
    i = check_input(0, len(search_IP), msg)
    if i == 0:
        return i
    else: 
        i = i - 1                                                                        
        myip = search_IP[i]                   
        def get_num(x):
            return str(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
        myip = str(myip)
        myip = get_num(myip)
        print "The IP we are going to connect to is %s" % myip
        return myip
#############################################################

############## ask user desired command function ###########
def des_comm():
    msg = """
If you would like to run a command, please enter the number:
\t1. Running configuration
\t2. Interfaces status
\t3. IP addressing interface information
\t4. OSPF Neighbors summary
\t5. Logging
\t6. Version/Uptime information
\t7. Enter a custom command

Otherwise, enter 0 to query the database again: """
    comm_opt = check_input(0, 7, msg)
    
    if comm_opt == 1:
        comm_opt = "show runn"
    elif comm_opt == 2:
        comm_opt = "show inter status"
    elif comm_opt == 3:
           comm_opt = "show ip inter brief"
    elif comm_opt == 4:
        comm_opt = "show ip ospf nei"
    elif comm_opt == 5:
        comm_opt = "show logging"
    elif comm_opt == 6:
        comm_opt = "show version"
    elif comm_opt == 7:
        comm_opt = raw_input("Type your command: ")
    return comm_opt
########################################################



################# ssh connection function #################
def ssh_conn(fhostname, fusern, fpassw, des_comm):
    try:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(fhostname, username = fusern, password = fpassw)
        #time.sleep()
        connection = session.invoke_shell()
        #time.sleep()
        connection.send("term len 0\n")
        connection.send("%s\n" % des_comm)
        time.sleep(1)
        output = connection.recv(65535)
        print output + "\n"
    except paramiko.AuthenticationException:
        print "Something went wrong during authentication, check username and password"        
        session.close()
    except:
        print "That box appears to be offline..."





print "####################################################################"
print "#                                                                  #"
print "#                       Lookup Ver 3.0 beta                        #"
print "#                                                                  #"
print "#                                                                  #"
print "#                   Developed by Victor Sanchez                    #"
print "#                                                                  #"
print "#                                                                  #"
print "#                                                                  #"
print "#            Press CTRL-C at any time to stop the script           #"
print "####################################################################"

sshlogin = raw_input("Give me your SSH username: ")
sshpass = getpass.getpass("Give me your SSH password: ")

while True:
    first = search_func()
    second = the_IP(first)
    if second == 0:
        pass
    else:
        third = des_comm()
        if third == 0:
            pass
        else:
            while True:
                fourth = ssh_conn(second, sshlogin, sshpass, third)
                third = des_comm()
                if third == 0:
                    break
              
