import json
from napalm import get_network_driver
from getpass import getpass
driver = get_network_driver('ios')
u_name = 'mwanjau'
ip_add = '172.17.121.29'
pwd = getpass('Password: ')
iosl2v =  driver(ip_add,u_name, pwd)
iosl2v.open()

bgp_neighbours = iosl2v.get_bgp_neighbors()
print(json.dumps(bgp_neighbours, indent=4))

iosl2v.close()

