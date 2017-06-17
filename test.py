#coding:utf-8

import  requests
import time

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    # 'cookie':'T_WM=aeee6a0b8b3b11ce4dad79442fcacdc0; ALF=1500199102; SCF=Auj49mreFq5enMS9W5VFU0yIBjKGjyZ1JqcdTESOzYAfBKV-3lG9RANUDNChFOC0NbCIkpIe7kEC7k1ZlhFnPCg.; SUB=_2A250R9vvDeRhGeBM6FQZ9yrFzz2IHXVXy-WnrDV6PUJbktBeLXfckW1Cz1p75RwJ052OqZ5-jpekZJpJJw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFsg31e.SLyy94khYdzU4SE5JpX5o2p5NHD95Qceoec1hMX1KBpWs4DqcjMeKe4i--Ri-zfi-8Fi--ciK.fiKysdgHEqNHEwBtt; SUHB=0YhRFPj8Qukyu1; SSOLoginState=1497607103; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D4093308865225942%26luicode%3D20000061%26lfid%3D4093308865225942'
             }


liststr=[]
for i in range(1,100):
    url ="https://m.weibo.cn/api/statuses/repostTimeline?id=4067563803082477&page="+str(i)
    liststr.append(url)

for i in liststr:
    print i
    req =requests.get(url=i,headers=headers)
    print req.url
    print req.text
    time.sleep(2)