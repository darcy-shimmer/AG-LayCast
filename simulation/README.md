# Simulation
This directory contains emulation code and some related scripts

## Dependency
[flask](https://github.com/pallets/flask)
> pip3 install flask

## Usage
### Servers information
You need to refine the information of hosts in the script (server.py).

> host_list=({'ip':'10.108.87.195', 'port':22, 'username':'', 'password':'','id':1},
             {'ip':'10.108.87.166', 'port':22, 'username':'', 'password':'','id':2},
             {'ip':'10.28.202.222', 'port':22, 'username':'', 'password':'','id':3},)

Start on port 8080
<font color=gray size=5>python3 server.py</font>
