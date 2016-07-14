import MySQLdb
import re
import time
import paramiko
import os
import getpass
import platform, os, subprocess
import log

#####################
# you will need to have dbconfig.txt in the directory, this file contains
# your database information in each line, like this:
#
# ip/hostname of database
# usrname
# password
# database name
#
# you will also need to have log.py in same directory, this is to colorize.
# if you wanna add commands, simply add them in des_comm function, and
# remember to add the elif condition for the new command you are adding.
####################


# define function that we will use to force user's input
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




# define database class
class Database:
    # read the lines of a file called dbconfig.txt which holds the database/login information
    dbfile = open("dbconfig.txt")
    # avoid reading the \n at the end of each line of dbconfig.txt
    host = dbfile.readline()[0:-1] 
    user = dbfile.readline()[0:-1]
    passwd = dbfile.readline()[0:-1]
    db = dbfile.readline()[0:-1]

    def __init__(self):
        # connect to the database using the credentials read from dbconfig.txt file
        self.connection = MySQLdb.connect(host = self.host,
                                            user = self.user,
                                            passwd = self.passwd,
                                            db = self.db)
    # query the database using passed "q" argument
    def query(self, q):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        # return fetchall (all matches)
        return cursor.fetchall()

    # close connection
    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    db = Database()




# define searching function to query the database
def search_func():
    msg = """
What do you want to search by:
    \t1. Search by Name
    \t2. Search by Address
    \t3. Search by City
    \t4. Search by Vendor

Enter the number you want to search by: """
    # use check_input function to get "bywhat" we will query the database
    bywhat = check_input(1, 4, msg)

    if bywhat == 1:
        bywhat = "Name"
    elif bywhat == 2:
        bywhat = "Address"
    elif bywhat == 3:
        bywhat = "City"
    elif bywhat == 4:
        bywhat = "Vendor"

    # get "what" the user wants to find
    what = raw_input("Search by %s: " % bywhat)
    # build query string to pass to the database query function
    q = ("SELECT * FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))
    # build query string to pass to the database query function but only for Mgmt IP column
    qIP = ("SELECT `Mgmt IP` FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))
    # store database query result in "search" variable to later iterate
    search = db.query(str(q))
    # this is just to enumerate the results
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
            # for each iteration, we will use subprocess to ping the 'Mgmt IP' element
            status = subprocess.call(
                ['ping', '-c1', '-W10', '-w2', entry['Mgmt IP']],
                stdout = open(os.devnull, 'wb'))
            if status == 0:
                print "is", 
                # this is to colorize the word UP
                log.infog("UP")
            else:
                print "is",
                # this is to colorize the word DOWN
                log.err("DOWN")
            print "----------------------------------------------------"
    # store the database query for the Mgmt IP column only in a variable called "search_IP"
    search_IP = list(db.query(str(qIP)))
    # return this variable to later use it to find out user's desired IP to connect to
    return search_IP




# define function to resolve user's desired IP to connect to
def the_IP(search_IP):
    msg = "If you would like to get an output from the box, enter the number for that box now.\nOtherwise, enter 0 to search again: "
    # i is the element position in search_IP list that user will connect to
    i = check_input(0, len(search_IP), msg)
    # if i is == 0, end function and return i, meaning user wants to go back to query step
    if i == 0:
        return i
    else: 
        i = i - 1
        # the IP user wants to connect to is search_IP's i position in the list                                                                        
        myip = search_IP[i]
        # function to get rid of undesired characters in the IP string                   
        def get_num(x):
            return str(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
        myip = str(myip)
        myip = get_num(myip)
        print "The IP we are going to connect to is %s" % myip
        # return the IP as a string that we will pass to the ssh_conn function
        return myip




# define function to get user's desired command to run on the box
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
    # return the desired command as a string, we will pass it to the ssh_conn function
    return comm_opt




# define ssh connection function to connect to the boxes
def ssh_conn(fhostname, fusern, fpassw, des_comm):
    try:
        # store paramiko ssh client func in variable called "session"
        session = paramiko.SSHClient()
        # ignore lack of host rsa key
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect to the box
        session.connect(fhostname, username = fusern, password = fpassw)
        # make it an interactive session
        connection = session.invoke_shell()
        # send term length 0 to the box and then user's command
        connection.send("term len 0\n")
        connection.send("%s\n" % des_comm)
        time.sleep(1)
        # store command's output in variable and then print it
        output = connection.recv(65535)
        print str(log.info(output)) + "\n"
        session.close()
    # if failed to authenticate
    except paramiko.AuthenticationException:
        print "Something went wrong during authentication, check username and password"        
        session.close()

############# end of functions declaration ############






# this is where program begins
splash = """
 ######################################################################
 ##                                                                  ##
 ##                      Lookup Ver 3.0 beta                         ##
 ##                                                                  ##
 ##                                                                  ##
 ##                   Developed by Victor Sanchez                    ##
 ##                                                                  ##
 ##                                                                  ##
 ##                                                                  ##
 ##            Press CTRL-C at any time to stop the script           ##
 ######################################################################"""
print (splash + "\n")


# get users username and pass
sshlogin = raw_input("Give me your SSH username: ")
sshpass = getpass.getpass("Give me your SSH password: ")


while True:
    # get user's desired query
    first = search_func()
    # get user's desired IP to connect to
    second = the_IP(first)
    # if user entered 0, start over
    if second == 0:
        pass
    # else, keep going
    else:
        # get users desired command to run
        third = des_comm()
        # if user entered 0, start all over
        if third == 0:
            pass
        # else, keep going
        else:
            # at this point we can keep running commands for a specific box as long as the user wants to
            while True:
                fourth = ssh_conn(second, sshlogin, sshpass, third)
                third = des_comm()
                # if user enters 0, start all from the beginning
                if third == 0:
                    break
              
