import time
import paramiko
import re
import sys
import os
import glob
import getpass

class paraconn:
	def __init__(self, hostname, usern, passw):
		self.session = paramiko.SSHClient()
		self.session.set_missin_host_key_policy(paramiko.AutoAddPolicy())

	def conn(self, hostname, usern, passw):
		conn = self.session.connect (hostname, username = usern, password = passw)
		conn = self.session.invoke_shell()

	def sendconn(self, comm):
		self.conn.send(comm + "\n")
		print self.conn.recv(65535)

	def closeconn(self):
		self.session.close()

if __name == "__main__":
	paraconn = paraconn()


usern = raw_input("Give me username (we will only need this once): ")
passw = getpass.getpass()

