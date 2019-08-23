import linecache
import urllib.request
import json
import time
import re

#according to queue of lon&lat, find 基站编号
def registerUrl(Index,outIndex):
    #try:
    url ="http://api.cellocation.com:81/recell/?lat="+str(Index)+"&lon="+str(outIndex)+"&n=10"
    #print(url)
    data = urllib.request.urlopen(url).read()
    return data
    #except Exception as e:
    #   print(e)

def extract():
    print('begin extract key values')
    line_cache = linecache.getlines('bjip_bs')
    with open('bjip_bs_ed', 'a') as ff:
        for i in range(1, len(line_cache)):
            print(line_cache[i])
            print(len(line_cache[i]))
            if len(line_cache[i]) > 3:
                c = re.sub('}, {', '}' + '\n' + '{', line_cache[i])
                ff.writelines(c)
    linecache.clearcache()
    print('extracted')

# according to bs' lac&ci&mnc, find exact location
def refind(mnc,lac,ci):
    #try:
    url = "http://api.cellocation.com:81/cell/?mcc=460&mnc=" + str(mnc) + "&lac=" + str(lac) + "&ci=" + str(ci) + "&output=json"
    data = urllib.request.urlopen(url).read()
    return data
    #except Exception as e:
    #    print(e)

def main():
    latrange = [i/10000.0 for i in range(398642,399694,200)]
    lonrange = [i/10000.0 for i in range(1163002,1164570,200)]
    for outindex in lonrange:
            for index in latrange:
                try:
                    data = registerUrl(index,outindex)
                except Exception as e:
                    print(e)
                    time.sleep(3600)
                    continue
                else:
                    value = json.loads(data)
                    valuee = str(value)
                    with open ('bjip_bs','a') as ff:
                        print(valuee)
                        print(index)
                        print(outindex)

                        ff.writelines(valuee)
                        ff.writelines('\n')
                    time.sleep(1)

    extract()

    lin_c = linecache.getlines('bjip_bs_ed')
    print('begin to find exact locations!')
    for i in range(1, len(lin_c)):
        _ci = re.findall(r"ci': (\d+),", lin_c[i])
        _lac = re.findall(r"lac': (\d+),", lin_c[i])
        _mnc = re.findall(r"mnc': (\d+),", lin_c[i])
        try:
            data = refind(_mnc[0],_lac[0],_ci[0])
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
                        with open('bs_location', 'a') as ff:
                            print(valuee)
                            ff.writelines(valuee)
                            ff.writelines('\n')
            time.sleep(1)
            linecache.clearcache()

if __name__ == "__main__":
    main()
