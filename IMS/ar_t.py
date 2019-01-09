import getpass
import telnetlib

HOST = "197.248.230.238"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
tn.write(b"system-view\n")
tn.write(b"voice\n")
tn.write(b"trunk-group safaricomTrunk\n")
tn.write(b"peer-address dns-a sip.safaricom.com 5060\n")
tn.write(b"quit\n")
tn.write(b"quit\n")
tn.write(b"quit\n")
tn.write(b"save\n")
tn.write("Y\n")
print("Config success")
print(tn.read_all().decode('ascii'))
