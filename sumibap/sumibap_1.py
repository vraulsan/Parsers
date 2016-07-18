import sys, os, glob, getpass, paramiko, telnetlib, time, re

# function to get the ssh credentials
def getSSHCredentials():
	sshlogin = raw_input("Give me your SSH username: ")
	sshpass = getpass.getpass("Give me your SSH password: ")
	return sshlogin, sshpass

	
# function to get hostname
def getHostname():
	while True:
		try:
			hostname = raw_input("Give me the hostname: ")
		except ValueError:
			continue
		else:
			# if CPR/cpr is within hostname string, return
			if "CPR" in hostname or "cpr" in hostname: 
				connectTo = 2                  # CPR's will use connectTo = 2
				return hostname, connectTo
				break
			# if BAP/bap is within hostname string, return
			elif "BAP" in hostname or "bap" in hostname:
				connectTo = 1                  # BAP's will use connectTo = 1
				return hostname, connectTo
				break
			else:
				continue
###########################################################################
# define function to telnet connect
def connectTelnet(hostname):
	port = 23
	timeout = 3
	connection = telnetlib.Telnet(hostname, port)
	# wait until we get prompt to Login
	connection.read_until("Login:", timeout)
	connection.write("tso\n")
	# wait until we get prompt to Password
	connection.read_until("Password:", timeout)
	connection.write("tso\n")
	print "Welcome to %s, type in your commands or \"exit\" at any time." % hostname
	command = raw_input("Command to run or exit: ")
	if 'exi' in command or command == 'exit':
		command = 'exit'	
		return connection
	else:
		connection.write(command + '\n')
		connection.write('log' + '\n')
		print connection.read_all()

# define function to interact with the BAPs (NOT USING DUE TO TELNET ISSUES)
#def naviTelnet(connection):
	#while True:
		#command = raw_input("Command to run or exit: ")
		#if "exit" in command or command == "exit":
			#connection.close()
			#command = "exit"
			#return command
			#break
		#else:
			#connection.write(command + "\n")
			#print connection.read_very_eager()
			#continue
#############################################################################

# SSH connection class
class connectSSH:
	def sessionSSH(self, hostname, usern, passw):
		try:
			self.session = paramiko.SSHClient()
			self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.session.connect(hostname, username = usern, password = passw)
			self.conn_established = self.session.invoke_shell()
			return self.conn_established
		except:
			print "This is the hostname we are attempting %s" % hostname
			print "Either you have wrong credentials or that CPR is unreachable"
			self.conn_failed = 0
			return self.conn_failed

	def ONUorCommandorBack(self, conn_established):
		self.ONUorCommandorBack = raw_input("Paste your ONU, type command or exit: ")
		if 'Slot' in self.ONUorCOmmandorBack or 'OLTPort' in self.ONUorCommandorBack:
			self.onu = re.findall(r'\d+', self.ONUorCommandorBack)
			self.onu = "1/" + self.onu[0] + '/' + self.onu[1] + '/' + self.onu[2]
			self.onu = """
			set cli pagination off\n
			show run epononu %s\n
			show onu %s\n
			show onu uniport %s\n""" % (self.onu, self.onu, self.onu)
			return self.onu
		elif 'ex' in self.ONUorCommandorBack:
			self.conn_established.close()
			self.conn_terminated = 0
			return self.conn_terminated

		else:
			self.command = self.ONUorCommandorBack
			self.command = """
			set cli pagination off\n
			%s\n""" % self.command
			return self.command

	def outputSSH(self, conn_established, what_to_run):
		self.conn_established.send(what_to_run)
		time.sleep(1)
		print self.conn_established.recv(65535)



usern, passw = getSSHCredentials()

while True:
	hostname, connectTo = getHostname()
	if connectTo == 2:
		while True:
			session = connectSSH()
			connect = session.sessionSSH(hostname, usern, passw)
			command = session.ONUorCommandorBack(connect)
			if command == 0:
					break
			else:
				session.outputSSH(connect, command)
	elif connectTo == 1:
		while True:
			exitOrcommand = connectTelnet(hostname)
			if exitOrcommand == 'exit':
				break
			else:
				continue
		

