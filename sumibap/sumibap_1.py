import sys, os, glob, getpass, paramiko, telnetlib, time

def getSSHCredentials():
	
# define function to get hostname
def getHostname():
	while True:
		try:
			hostname = raw_input("Give me the hostname: ")
		except ValueError:
			continue
		else:
			break
	if "CPR" or "cpr" in hostname:
		connectTo = 1
	elif "BAP" or "bap" in hostname:
		connecTo = 2
	return hostname, connectTo

###########################################################################
# define function to telnet connect
def connectTelnet(hostname, usern, passw):
	port = 23
	timeout = 3
	connection = telnetlib.Telnet(hostname, port)
	connection.read_until("Login:", timeout)
	connection.write("tso\n")
	connection.read_until("Password:", timeout)
	connection.write("tso\n")
	print "Welcome to %s, type in your commands or \"exit\" at any time." % hostname
	return connection

# define function to interact with the BAPs
def naviTelnet(connection):
	while True:
		command = raw_input("Command to run: ")
		if "exit" in command or command == "exit":
			connection.close()
		else:
			connection.write(command + "\n")
			print connection.read_very_eager()
#############################################################################
