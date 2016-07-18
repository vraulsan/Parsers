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
    connection.write("tso\r\n")
    # wait until we get prompt to Password
    connection.read_until("Password:", timeout)
    connection.write("tso\r\n")
    print "Welcome to %s, type in your commands or \"exit\" at any time." % hostname
    command = raw_input("Command to run or exit: ")
    if 'exi' in command:
        command = 0
        connection.close()
        return command
    elif 'loge' in command:
        command = "show logevent all -n 100"
        connection.write(command + '\r\n')
        connection.write('logout' + '\r\n')
        output = connection.read_all()
        connection.close()
        print output
    else:
        connection.write(command + '\r\n')
        connection.write('logout' + '\r\n')
        output = connection.read_all()
        connection.close()
        print output

#############################################################################

# SSH connection class
class connectSSH:
    def sessionSSH(self, hostname, usern, passw):
        try:
            self.session = paramiko.SSHClient()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.session.connect(hostname, username = usern, password = passw)
            self.conn_established = self.session.invoke_shell()
        except paramiko.AuthenticationException:
            print "Authentication failed, please verify your crendetials..."
            self.conn_failed = 0
            return self.conn_failed
        except:
            print "Either that hostname is unreachable or something else failed, please try again..."
            self.conn_failed = 1
            return self.conn_failed
        return self.conn_established

    def ONUorCommandorBack(self, conn_established):
        self.ONUorCommandorBack = raw_input("Paste your ONU, type command or exit: ")
        if 'Slot' in self.ONUorCommandorBack or 'OLTPort' in self.ONUorCommandorBack:
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


print "####################################################################"
print "#                                                                  #"
print "#                      SUMIBAP Ver 1.0 beta                        #"
print "#                 (useful when doing Spectrum)                     #"
print "#                                                                  #"
print "#                  Developed by Victor Sanchez                     #"
print "#                                                                  #"
print "#                        for BHN ATS Team                          #"
print "#                                                                  #"
print "#            Press CTRL-C at any time to stop the script           #"
print "####################################################################"


usern, passw = getSSHCredentials()

while True:
    hostname, connectTo = getHostname()
    if connectTo == 2:
        while True:
            session = connectSSH()
            connect = session.sessionSSH(hostname, usern, passw)
            if connect == 0:
                usern, passw = getSSHCredentials()
                break
            elif connect == 1:
                break
            command = session.ONUorCommandorBack(connect)
            if command == 0:
                break
            else:
                session.outputSSH(connect, command)
    elif connectTo == 1:
        while True:
            exitOrcommand = connectTelnet(hostname)
            if exitOrcommand == 0:
                #print exitOrcommand
                break
            else:
                continue
