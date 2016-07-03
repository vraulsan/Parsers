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
    q = "SELECT * FROM  `customers` WHERE `City` REGEXP " + " \'" + what_city + "\' " + " LIMIT 0 , 30"
    search = db.query(q)
    for entry in search:
        print "Found %s" % entry['Name'],
        print "in %s" % entry['City'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']


# define function for when searching by Name
def byname():
    what_name = raw_input("Search by name: ")
    q = "SELECT * FROM  `customers` WHERE `Name` REGEXP " + " \'" + what_name + "\' " + " LIMIT 0 , 30"
    search = db.query(q)
    for entry in search:
        print "Found %s" % entry['Name'],
        print "in %s" % entry['City'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']


# define function for when searching by Name
def byaddress():
    what_address = raw_input("Search by address: ")
    q = "SELECT * FROM  `customers` WHERE `Address` REGEXP " + " \'" + what_address + "\' " + " LIMIT 0 , 30"
    search = db.query(q)
    for entry in search:
        print "Found %s" % entry['Name'],
        print "at %s" % entry['Address'], 
        print "with Mgmt IP of %s" % entry['Mgmt IP']

# display Menu with options for searching
option = input("""
Please enter the number for your desired search:
1.  Search by Name
2.  Search by Address
3.  Search by City
""")

# call the functions
if option == 1:
    byname()
if option == 2:
    byaddress()
if option == 3:
    bycity()
