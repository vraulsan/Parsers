##############################################################################################
###### Will ask user for desired search method, bring up the matched customers ###############
###### and ask whether we want to connect to the equipment to pull information ###############
#############################################################################################

import MySQLdb
import re

######################### Lets build our Class ################################

class Database:
    host = "hostname/ip"
    user = "ubuntu-vm"
    passwd = "passwd"
    db = "fireprotocol"
    
    # build the constructor
    # argument "self" refers to the current instance of the class
    def __init__(self):
        self.connection = MySQLdb.connect(host = self.host,
                                            user = self.user,
                                            passwd = self.passwd,
                                            db = self.db)
    # define the query function
    def query(self, q):
        # create a cursor to query the records in the database
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        # return all results from the query
        return cursor.fetchall()

    #  define the query function for fetch one (not using right now)
	def queryone(self, q):
		cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(q)
		return cursor.fetchone()

    # and then close the connection with this other function
    def __del__(self):
        self.connection.close()
        
########################## End of the Class ###################################
if __name__ == "__main__":
    db = Database()

# ask the user what they want to search by
bywhat = input("""
What do you want to search by:
	1. Search by Name
	2. Search by Address
	3. Search by City
	4. Search by Vendor
	""")
# transform the user input to the proper string to pass to the query db.query function
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

# ask the user what is the value of their search method
what = raw_input("Search by %s: " % bywhat)

# define the query string for all rows all data
q = ("SELECT * FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))
# define the query string for all rows Mgmt IP
qIP = ("SELECT `Mgmt IP` FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))

# query the DB using q string
search = db.query(str(q))

# use for loop to iterate through values for each position of the table
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

######################### Figure out IP to connect to #############################
# query the DB using qIP string and then conver to a list
search_IP = list(db.query(str(qIP)))
# ask the user what box they want to get output from
i = input("\nIf you would like to get an output from the box, enter the number for that box now :")
# use this i variable to figure out the right list position 
i = i - 1                                                                        
# use variable i to extract the list position, meaning the desired IP
myip = search_IP[i]                   
# function to extract the IP number only and get it as a string
def get_num(x):
	return str(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
# transform list position into a string so we can put pass it to the get_num function
myip = str(myip)
myip = get_num(myip)
print "The IP we are going to connect to is %s" % myip
######################### Figure out IP to connect to #############################

option = input("""
	\t1. Running configuration
	\t2. Interfaces status
	\t3. IP addressing interface information
	\t4. OSPF Neighbors summary
	\t5. Logging
	\t6. Version/Uptime information
	Please enter an option from above: """)
