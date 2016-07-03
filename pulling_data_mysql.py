##############################################################################################
###### Will ask user for desired search method, bring up the matched customers ###############
###### and ask whether we want to connect to the equipment to pull information ###############
#############################################################################################

import MySQLdb

######################### Lets build our Class ################################

class Database:
    host = "hostname/ip"
    user = "ubuntu-vm"
    passwd = "pass"
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

# define the query string
q = ("SELECT * FROM  `customers` WHERE `%s` REGEXP \'%s\' LIMIT 0 , 30" % (bywhat, what))
	#return q

# store the query output in variable named search
search = db.query(str(q))

# use for loop to print out values for each position of the table
for entry in search:
        print "Found: %s" % entry['Name'],
        print "at %s" % entry['Address'], 
        print "using %s" % entry['Vendor'],
        print "in %s" % entry['City'],
        print "with Mgmt IP of %s" % entry['Mgmt IP']
