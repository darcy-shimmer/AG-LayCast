import linecache
import urllib.request
import json
import time
import re

#according to queue of lat&lon, find wifi's mac
def registerUrl(Index,outIndex):
    #try:
    url ="http://api.cellocation.com:81/rewifi/?lat="+str(Index)+"&lon="+str(outIndex)+"&n=10"
    #print(url)
    data = urllib.request.urlopen(url).read()
    return data
    #except Exception as e:
    #   print(e)

def extract():
    print('begin extract key values')
    line_cache = linecache.getlines('bjwifi_mac')
    with open('bjwifi_mac_ed', 'a') as ff:
        for i in range(1, len(line_cache)):
            print(line_cache[i])
            print(len(line_cache[i]))
            if len(line_cache[i]) > 3:
                c = re.sub('}, {', '}' + '\n' + '{', line_cache[i])
                ff.writelines(c)
    linecache.clearcache()
    print('extracted')

#according to wifi's mac, find exact location
def refind(MAC):
    #try:
    url = "http://api.cellocation.com:81/wifi/?mac=" + str(MAC) + "&output=json"
    data = urllib.request.urlopen(url).read()
    return data
    #except Exception as e:
    #    print(e)

def main():
    latrange = [i/10000.0 for i in range(398642,399694,50)]
    lonrange = [i/10000.0 for i in range(1163002,1164570,50)]
    for outindex in lonrange:
        for index in latrange:
            try:
                data = registerUrl(index, outindex)
            except Exception as e:
                print(e)
                time.sleep(3600)
                continue
            else:
                value = json.loads(data)
                valuee = str(value)
            with open('bjwifi_mac', 'a') as ff:
                print(valuee)
                print(index)
                print(outindex)

                ff.writelines(valuee)
                ff.writelines('\n')
            time.sleep(1)

    extract()

    lin_c = linecache.getlines('bjwifi_mac_ed')
    print('begin!')
    for i in range(1, len(lin_c)):
        mac = re.findall(r"mac': '(..:..:..:..:..:..)'", lin_c[i])
        print(mac[0])
        try:
            data = refind(mac[0])
        except Exception as e:
            print(e)
            time.sleep(3600)
            continue
        else:
            value = json.loads(data)
            valuee = str(value)
            print(valuee)
            if re.findall('10000', valuee) != ['10000']:
                if re.findall('10001', valuee) != ['10001']:
                    if re.findall(": '北京市", valuee) == [": '北京市"]:
                        with open('ap_location', 'a') as ff:
                            print(valuee)
                            print(mac)
                            ff.writelines(valuee)
                            ff.writelines('\n')
            time.sleep(1)
            linecache.clearcache()

if __name__ == "__main__":
    main()
