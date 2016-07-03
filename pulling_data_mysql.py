##############################################################################################
###### Will ask user for desired search method, bring up the matched customers ###############
###### and ask whether we want to connect to the equipment to pull information ###############
#############################################################################################

import MySQLdb

######################### Lets build our Class ################################

class Database:
    host = "52.20.131.2"
    user = "ubuntu-vm"
    passwd = "kornkid182"
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

# define function for when searching by City
def bycity():
    what_city = raw_input("Search by city: ")
    q = ("SELECT * FROM  `customers` WHERE `City` REGEXP \'%s\' LIMIT 0 , 30" % what_city)
    search = db.query(str(q))
    for entry in search:
        print "Found: %s" % entry['Name'],
        print "in %s" % entry['City'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']


# define function for when searching by Name
def byname():
    what_name = raw_input("Search by name: ")
    q = ("SELECT * FROM  `customers` WHERE `Name` REGEXP \'%s\' LIMIT 0 , 30" % what_name)
    search = db.query(str(q))
    for entry in search:
        print "Found: %s" % entry['Name'],
        print "in %s" % entry['City'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']


# define function for when searching by Name
def byaddress():
    what_address = raw_input("Search by address: ")
    q = ("SELECT * FROM  `customers` WHERE `Address` REGEXP \'%s\' LIMIT 0 , 30" % what_address)
    search = db.query(str(q))
    for entry in search:
        print "Found: %s" % entry['Name'],
        print "at %s" % entry['Address'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']


# define function for when searching by Vendor
def byvendor():
    what_vendor = raw_input("Search by Vendor: ")
    q = ("SELECT * FROM  `customers` WHERE `Vendor` REGEXP \'%s\' LIMIT 0 , 30" % what_vendor)
    search = db.query(str(q))
    for entry in search:
        print "Found: %s" % entry['Name'],
        print "at %s" % entry['Address'], 
        print "using %s" % entry['Vendor'],
        print "with Mgmt IP of %s" % entry['Mgmt IP']

# display Menu with options for searching
msg = """
    Please enter the number for your desired search:
        1.  Search by Name
        2.  Search by Address
        3.  Search by City
        4.  Search by Vendor
    """
option = input(msg)
while option != 1 and option != 2 and option != 3 and option != 4:
    option = input(msg)

# call the functions
if option == 1:
    byname()
if option == 2:
    byaddress()
if option == 3:
    bycity()
if option == 4:
    byvendor()
