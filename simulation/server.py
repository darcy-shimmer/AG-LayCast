import paramiko
import re
import time
import sys
import json

from flask import make_response
from flask import Flask
from flask import request
#from flask import abort
from flask import jsonify
from flask import Response
from flask_cors import *

app = Flask(__name__)
CORS(app, resources=r'/*')

# the information of hosts
host_list=({'ip':'10.108.87.195', 'port':22, 'username':'', 'password':'','id':1},
           {'ip':'10.108.87.166', 'port':22, 'username':'', 'password':'','id':2},
           {'ip':'10.28.202.222', 'port':22, 'username':'', 'password':'','id':3},)

ssh_host = paramiko.SSHClient()

ssh_host.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# fet the memory information of each host
def get_memoryInf(ssh_list):
    totalmem = [];
    freemem = [];
    use = [];
    for inx, host in enumerate(ssh_list):
        ssh_host.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        print(host['ip'])
        stdin, stdout, stderr = ssh_host.exec_command('cat /proc/meminfo')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue

        str_total = re.search('MemTotal:.*?\n', str_out).group()
        print(str_total)
        totalmem.append(re.search('\d+',str_total).group())

        str_free = re.search('MemFree:.*?\n', str_out).group()
        print(str_free)
        freemem.append(re.search('\d+',str_free).group())
        use.append(round((float(totalmem[inx])-float(freemem[inx]))/float(totalmem[inx]), 2))
        print('memory usage：'+ str(use[inx]))
        ID.append(host['id'])

        ssh_host.close()

    return totalmem, freemem, use, ID

# get the cpu usage of each host
def get_cpuInf(ssh_list):
    cpu_usage = [];
    for inx, host in enumerate(ssh_list):
        ssh_host.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        print(host['ip'])
        stdin, stdout, stderr = ssh_host.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle1 = cpu_time_list[3]
            total_cpu_time1 = 0
            for index, name in enumerate(cpu_time_list):
                 total_cpu_time1 = total_cpu_time1 + int(name)

        time.sleep(2)

        stdin, stdout, stderr = ssh_host.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle2 = cpu_time_list[3]
            total_cpu_time2 = 0
            for index, name in enumerate(cpu_time_list):
                total_cpu_time2 = total_cpu_time2 + int(name)

        cpu_usage.append(round(100 -(float(cpu_idle2) - float(cpu_idle1))*100 / (total_cpu_time2 - total_cpu_time1), 3))
        print('当前CPU使用率为：' + str(cpu_usage[inx]))
        ID.append(host['id'])

        ssh_host.close()
    return cpu_usage, ID

# get the dist usage of each host
def get_distInf(ssh_list):
    usage = []
    for host in ssh_list:
        ssh_host.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        print(host['ip'])
        stdin, stdout, stderr = ssh_host.exec_command('df -lm')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue
        info = re.findall('\d+', str_out)
        usage.append(info[59])
        ID.append(host['id'])

        ssh_host.close()
    return usage, ID

# get network out-/in-throughput of each host
def get_netInf(ssh_list):
    sent = []
    receive = []
    recRate = []
    senRate = []
    for host in ssh_list:
        ssh_host.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        print(host['ip'])
        stdin, stdout, stderr = ssh_host.exec_command('cat /proc/net/dev')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue
        info = re.findall('\d+', str_out)
        receive.append(info[19])
        sent.append(info[27])

        time.sleep(1)

        stdin, stdout, stderr = ssh_host.exec_command('cat /proc/net/dev')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue
        info = re.findall('\d+', str_out)

        receive.append(info[19])
        sent.append(info[27])

        recRate.append(int(receive[1]) - int(receive[0]))
        senRate.append(int(sent[1]) - int(sent[0]))
        ID.append(host['id'])

        ssh_host.close()
    return senRate, recRate, ID

@app.route('/')
def start():
  return 'Hello world!'

@app.route('/host/mem', methods=['GET','POST'])
def hostMemory():
  try:
    totalmem, freemem, use, ID = get_memoryInf(Cloud_list)
    print (1)
  except IOError:
    response = make_response(jsonify({'value':'no input.','code':400}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
  else:
    if(int(totalmem)<1):
      response = make_response(jsonify({'value':'no input.','code':400}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'POST'
      response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
      return response

    reText = []
    for inx, usage in enumerate(use):
        reText.append({'total': totalmem[inx],
                       'free': freemem[inx],
                       'usage': usage,
                       'id':ID[inx]})

    response = make_response(jsonify({'value': reText,'code':200}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route('/host/cpusage', methods=['GET','POST'])
def hostCPU():
  try:
    usage, ID = get_cpuInf(host_list)
    print (1)
  except IOError:
    response = make_response(jsonify({'value':'no input.','code':400}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
  else:
    if(len(usage)<1):
      response = make_response(jsonify({'value':'no input.','code':400}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'POST'
      response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
      return response

    reText = []
    for inx, use in enumerate(usage):
        reText.append({'usage': use,
                       'id':ID[inx]})

    response = make_response(jsonify({'value': reText,'code':200}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route('/host/dist', methods=['GET','POST'])
def hostDist():
  try:
    usage, ID = get_distInf(host_list)
  except IOError:
    response = make_response(jsonify({'value':'no input.','code':400}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
  else:
    if(len(usage)<1):
      response = make_response(jsonify({'value':'no input.','code':400}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'POST'
      response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
      return response

    reText = []
    for inx, use in enumerate(usage):
        reText.append({'usage': use,
                       'id':ID[inx]})

    response = make_response(jsonify({'value': reText,'code':200}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

@app.route('/host/net', methods=['GET','POST'])
def hostNet():
  try:
    sent, receive, ID = get_netInf(host_list)
  except IOError:
    response = make_response(jsonify({'value':'no input.','code':400}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response
  else:
    if(len(sent)<1):
      response = make_response(jsonify({'value':'no input.','code':400}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'POST'
      response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
      return response

    reText = []
    for inx, sen in enumerate(sent):
        reText.append({'sent': sen,
                       'receive': receive[inx],
                       'id':ID[inx]})

    response = make_response(jsonify({'value': reText,'code':200}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080,debug=True)
