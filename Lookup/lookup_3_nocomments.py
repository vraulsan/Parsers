import MySQLdb
import re
import time
import paramiko
import sys
import os
import glob
import getpass


######### define database class ###############
class Database:
    host = "ip/hostname"
    user = "ubuntu-vm"
    passwd = "passw"
    db = "fireprotocol"
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
    bywhat = input("""
What do you want to search by:
    \t1. Search by Name
    \t2. Search by Address
    \t3. Search by City
    \t4. Search by Vendor
    """)
    if bywhat == 1:
        bywhat = "Name"
    elif bywhat == 2:
        bywhat = "Address"
    elif bywhat == 3:
        bywhat = "City"
    elif bywhat == 4:
        bywhat = "Vendor"
    else: 
        print "Wrong input, try again."
        exit()

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
            print "\n\tMgmt IP: %s" % entry['Mgmt IP']
            print "----------------------------------------------------"
    search_IP = list(db.query(str(qIP)))
    return search_IP
################################################################
def the_IP(search_IP):
    i = input("\nIf you would like to get an output from the box, enter the number for that box now.\nOtherwise, enter 0 to search again: ")
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
    comm_opt = input("""
If you would like to run a command, please enter the number:
\t1. Running configuration
\t2. Interfaces status
\t3. IP addressing interface information
\t4. OSPF Neighbors summary
\t5. Logging
\t6. Version/Uptime information
\t7. Enter a custom command

Otherwise, enter 0 to query the database again.""")
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



username = "login"
passw = "passw"



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
                fourth = ssh_conn(second, username, passw, third)
                third = des_comm()
                if third == 0:
                    break
