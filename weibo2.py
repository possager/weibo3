#_*_coding:utf8_*_
import requests
import cookielib
import time
import pymongo
import random
import MySQLdb
import threading
import json
import datetime

limitDown=37028
limitUP=38000

proxyInUsing=[]
proxyWouldChange=set([])
proxyWouldChangeheaders=set([])

class CookieGet2:
    def __init__(self):
        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',charset='utf8')
        self.cursor=self.connect.cursor()

        self.headers={
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
            # 'cookie':'login_sid_t=aa544db4f87986a0a38f267cead3c787; _s_tentry=-; Apache=7523975442007.387.1497494316556; SINAGLOBAL=7523975442007.387.1497494316556; ULV=1497494316560:1:1:1:7523975442007.387.1497494316556:; SUB=_2AkMuHXwCf8NxqwJRmP4XxG7maIhzyAzEieKYQY3ZJRMxHRl-yT83qhNTtRCl4TR4Z99V0GM3KtjTss_8evN6_w..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWLphwKCinbC-wHgV-iMLQs',
            'referer':'https://m.weibo.cn/status/EslDScVTn?luicode=20000061&lfid=4118572374788617&featurecode=20000180',
            # 'cookie':'_T_WM=aeee6a0b8b3b11ce4dad79442fcacdc0; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D4067563803082477%26luicode%3D10000011%26lfid%3D1005055526045431'
        }

    def getZhuanFa(self,urlZhuanfa,proxyInGetZhuanFa):
        session2 = requests.session()

        connectZhuanFa = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', charset='utf8')
        cursor = connectZhuanFa.cursor()



        UserAgentlist=['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
                       'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                       'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1']


        headers1 = {
            'User-Agent': UserAgentlist[random.randint(0,len(UserAgentlist)-1)],
        }
        headers2={
            'User-Agent':UserAgentlist[random.randint(0,len(UserAgentlist)-1)],
                    }
        if len(proxyWouldChangeheaders)>3:
            session2.headers=headers1
            listcookielisthere=list(proxyWouldChangeheaders)
            session2.headers['cookie']=listcookielisthere[random.randint(0,len(proxyWouldChangeheaders)-1)]
        else:
            session2.headers=headers2
        urlsss = urlZhuanfa
        continue1=0
        while continue1==0:
            try:
                response2 = session2.request(method='GET', url=urlsss)
                print response2.status_code
                datajson = json.loads(response2.text)
                cookievalues=''
                cookievalues2=''
                response2.cookies
                for i in response2.cookies:
                    cookievalues+=i.name+'='+i.value+';'#因为报错说:unhashable type: 'RequestsCookieJar'

                for jj in session2.cookies:
                    cookievalues2+=jj.name+'='+jj.value+';'


                print cookievalues
                proxyWouldChangeheaders.add(cookievalues)
                proxyWouldChangeheaders.add(cookievalues2)
                if response2.status_code < 400 and len(datajson['data'])>0:
                    continue1=1
                else:
                    time.sleep(random.randint(1,3))
            except Exception as e:
                print e
                try:

                    sqlupdatecantbeuse='DELETE FROM proxy.proxy_could_be_use_by_weibo WHERE proxyip="%s"'%(proxyInGetZhuanFa)
                    # cursor.execute(sqlupdatecantbeuse)
                    # connectZhuanFa.commit()
                except Exception as e:
                    print 'error'

                return
        try:
            ceshi=datajson['data']
        except Exception as e:
            print e
            return


        for json1 in datajson['data']:
            try:#我也不知道为什么要写这么多try,反正就是写
                id = json1['id']
                text = json1['text']
                # source=json1['source']
                if u'分钟前' in json1['created_at']:
                    d = time.time() - 60*int(json1['create_at'].replace('分钟前'))
                    created_at= time.strftime('%Y-%m-%d %H:%M', time.localtime(d))
                elif u'今天' in json1['created_at']:
                    created_at=str(datetime.date.today())+json1['created_at'].replace(u'今天','')
                else:
                    created_at='2017-'+json1['created_at']

                raw_text=''

                try:
                    raw_text = json1['raw_text']
                except Exception as e:
                    print e
                userdata = json1['user']

                userid = userdata['id']
                userprofile_url = userdata['profile_url']
                userscreen_name = userdata['screen_name']
                userverified = userdata['verified']
                userverified_type = userdata['verified_type']

                print id, text, created_at, userid, userscreen_name, userprofile_url
                try:
                    sqlZhuanfalist='INSERT INTO weibo.weiboEslDScVTn (postid,zhuanfa_text,raw_text,create_at,userid,userscreen_name,userprofile_url,userverified,userverified_type)' \
                                   'VALUE (%d,"%s","%s","%s",%d,"%s","%s",%d,%d)'%(
                        id,text,raw_text,created_at,userid,userscreen_name,userprofile_url,userverified,userverified_type
                    )
                    print sqlZhuanfalist
                    cursor.execute(sqlZhuanfalist)
                    connectZhuanFa.commit()
                except Exception as e:
                    print e
            except Exception as e:
                print e


        time.sleep(random.randint(1,2))
        # proxyInUsing.remove(proxyInGetZhuanFa)


    # def textduoxiancheng(self,sb,sq):
    #     print sb
    #     print sq



    def run(self,url1,limit1=1,limit2=2):
        cookie1=cookielib.LWPCookieJar()
        session1=requests.session()
        session1.headers=self.headers
        session1.cookies=cookie1


        for url11 in url1:
            response1=session1.request(method='GET',url=url11)

        sqlgetproxy = 'SELECT proxyip,proxyport,proxytype FROM proxy.proxy_could_be_use_by_weibo'

        connectrun = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', charset='utf8')
        cursorrun = connectrun.cursor()
        cursorrun.execute(sqlgetproxy)
        connectrun.commit()
        proxylist = []
        for proxy1 in cursorrun.fetchall():
            dict1 = {
                proxy1[2]: proxy1[2] + '://' + proxy1[0] + ':' + proxy1[1]
            }
            print dict1
            proxylist.append(dict1)



        threadlist=[]
        visitnum=limitDown

        # proxylistIsUsing=[]

        urllist=self.yiedlurl()
        while threadlist or urllist:
            for threadi in threadlist:
                if not threadi.is_alive():
                    threadlist.remove(threadi)
            while len(threadlist)< 1 and urllist:
                thisurl=urllist.pop()
                proxyrandom=None
                while proxyrandom is None or proxyrandom in proxyInUsing:
                    proxyrandom = proxylist[random.randint(0, len(proxylist)-1)]
                proxyInUsing.append(proxyrandom)
                thread2=threading.Thread(target=self.getZhuanFa,args=(thisurl,proxyrandom))
                thread2.setDaemon(True)
                thread2.start()
                threadlist.append(thread2)
                print len(threadlist)
            time.sleep(2)





    def yiedlurl(self):
        urllistall=[]
        for pagenum in range(limitDown, limitUP):
            urlsss = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4067563803082477&page=' + str(pagenum)
            urllistall.insert(0,urlsss)
        return urllistall


if __name__ == '__main__':
    thisclass=CookieGet2()
    lsit1 = [
        'http://m.weibo.cn/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom&filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom&filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/status/ED9oalVvo',
        'http://weibo.com/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/statuses/extend?id=4093308865225942',
        'https://m.weibo.cn/api/comments/show?id=4093308865225942&page=1',
        'https://m.weibo.cn/api/config',

    ]
    thisclass.run(lsit1)