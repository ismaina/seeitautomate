
import telnetlib
import sys
import getpass

HOST = "197.248.230.238"

PASSWORD = getpass.getpass()
pw = 'Admin@123'

telnet = telnetlib.Telnet(HOST)

telnet.read_until("Password: ")
telnet.write(pw + "\n")

telnet.write("display interface brief\n")
telnet.write("quit\n")

print telnet.read_all()
