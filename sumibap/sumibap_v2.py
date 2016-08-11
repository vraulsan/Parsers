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
            hostname = hostname.replace(' ', '')
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
    return connection

def commandsTelnet(connection, command):
    if 'loge' in command:
        command = "show logevent all -n 100"
        connection.write(command + '\r\n')
        time.sleep(2)
        output = connection.read_very_eager()
        print output
    elif ':' in command:
        showlog = "show logevent all -n 100"
        connection.write(showlog + '\r\n')
        time.sleep(2)
        output = connection.read_very_eager()
        for line in output.splitlines():
            if command in line:
                print line
    elif 'find-vlan' in command:
        command = command.split()
        cust = command[1].upper()
        connection.write("show vlan all\r\n")
        time.sleep(2)
        output = connection.read_very_eager()
        for line in output.splitlines():
            if cust in line:
                print line
    else:
        connection.write(command + '\r\n')
        time.sleep(1)
        output = connection.read_very_eager()
        print output

#############################################################################

# SSH connection class
def sessionSSH(hostname, usern, passw):
    try:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname, username = usern, password = passw, timeout=1000)
        conn_established = session.invoke_shell()
        conn_established.keep_this = session
    except paramiko.AuthenticationException:
        print "Authentication failed, please verify your crendetials..."
        conn_failed = 0
        return conn_failed
    except:
        print "Either that hostname is unreachable or something else failed, please try again..."
        conn_failed = 1
        return conn_failed
    return conn_established

def ONUorCommandorBack():
    ONUorCommandorBack = raw_input("Paste your ONU, type command or exit: ")
    if 'Slot' in ONUorCommandorBack or '/ONU' in ONUorCommandorBack:
        onu = re.findall(r'\d+', ONUorCommandorBack)
        onu = "1/" + onu[0] + '/' + onu[1] + '/' + onu[2]
        onu = """
        show run epononu %s\n
        show onu %s\n
        show onu uniport %s\n""" % (onu, onu, onu)
        return onu
    elif 'exit' in ONUorCommandorBack:
        conn_terminated = 0
        return conn_terminated
    else:
        return ONUorCommandorBack



###################################################################################
###################################################################################

logo = """

                                                                
                .,:;;;;:,.               .,;;;;;:,.                 
           .:;;;:,.          ...,,...           .,;;;;,             
        .:;;;,      .,:;;;;;;;;;;;;;;;;;;;;:,        ,;;;,          
       :;;,     .:;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,.     .:;;,        
     .;;;.    :;;;;;;;;;;,               ,;;;;;;;;;,     .;;:       
    .;;.    :;;;;;;;;,                       ,;;;;;;;:     :;;      
   .;;.   :;;;;;;;.                             ,;;;;;;:.   ,;:     
   ,;.  .:;;;;;:.       .:;;;;;;;;;;;;;:,         ,;;;;;;.   ,;,    
   ;:   ;;;;;;.      .;;;;;;;;;;;;;;;;;;;;;,        ,;;;;;,   :,    
   :  .;;;;;;      ,;;;;;;;;;;;;;;;;;;;;;;;;;,       .;;;;;,  .;    
   .  :;;;;:      ;;;;;;;;:,         .:;;;;;;;;,       ;;;;;.  :    
     .;;;;:     ,;;;;;;;.                ;;;;;;;:      .;;;;;       
     ;;;;;.    .;;;;;;:                   .;;;;;;;      .;;;;.      
     ;;;;:     ;;;;;;;    Sumibap_v1.py    .;;;;;;.      ;;;;:      
    .;;;;,    ,;;;;;;                       ,;;;;;:      :;;;;      
    ,;;;;.    ;;;;;;:      Developed by      ;;;;;;.     :;;;;.     
    ,;;;;.    ;;;;;;:                        ;;;;;;.     :;;;;.     
    .;;;;,    ,;;;;;:     Victor Sanchez    .;;;;;:      :;;;;      
    .;;;;:    .;;;;;;:                      ;;;;;;.      :;;;;      
     ;;;;;     ,;;;;;;,    for ATS Team    ;;;;;;;      .;;;;,      
     .;;;;:     ,;;;;;;;.                :;;;;;;:.      :;;;;       
   .  :;;;;:     .;;;;;;;;,.          ,:;;;;;;;:       :;;;;,  ,    
   :  .;;;;;,      :;;;;;;;;;;;:::;;;;;;;;;;;:.       :;;;;:  .;    
   ;,  .;;;;;;       .;;;;;;;;;;;;;;;;;;;;;:.       .;;;;;:   ::    
   :;   .:;;;;;,        .;;;;;;;;;;;;;;;:          :;;;;;,   .;,    
   .;;    :;;;;;;,           .,,,,,.             :;;;;;;.   .;:     
    .;;    .:;;;;;;:.                         ,;;;;;;;.    .;;.     
     .;;:     :;;;;;;;;:.                 .:;;;;;;;:.    .:;;       
      .;;;,     .:;;;;;;;;;;;;:,,,,,:;;;;;;;;;;;;.      :;;:        
        .:;;:.     .,:;;;;;;;;;;;;;;;;;;;;;;;,.      .;;;:.         
           ,:;;:,.        ,,,::;;;;;::,,.        .:;;;:.            
               .,::;;;:,.                .,,:;;;::,.                
 """                                                                   
 

print logo

usern, passw = getSSHCredentials()

while True:
    hostname, connectTo = getHostname()
    if connectTo == 2:
        while True:
            connect = sessionSSH(hostname, usern, passw)
            if connect == 0:
                usern, passw = getSSHCredentials()
            elif connect == 1:
                break
            else:
                connect.send("set cli pagination off\n")
                while True:
                    command = ONUorCommandorBack()
                    if command == 0:
                        connect.close()
                        break
                    else:
                        connect.send(command + '\n')
                        time.sleep(0.5)
                        print connect.recv(65535)
            break
    elif connectTo == 1:
        telconn = connectTelnet(hostname)
        while True:
            telcomm = raw_input("Command to run or exit: ")
            if 'exi' in telcomm:
                break
            else:
                commandsTelnet(telconn, telcomm)


