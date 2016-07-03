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

#define function for when searching by city
def bycity(what_city):
    what_city = raw_input("Search by city: ")
    q = "SELECT * FROM  `customers` WHERE `City` REGEXP " + " \'" + what_city + "\' " + " LIMIT 0 , 30"
    search = db.query(q)
    for entry in search:
        print "Found %s" % entry['Name'] ,
        print "in %s" % entry['City'] , 
        print ", with Mgmt IP of %s" % entry['Mgmt IP']

