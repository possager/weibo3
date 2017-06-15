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
# from multiprocessing import pool
from bs4 import BeautifulSoup

limitDown=1000
limitUP=4300
proxyInUsing=[]

# class  weibo:
#     def __init__(self):
#

proxyWouldChange=set([])


class CookieGetWithoutLogin:
    def __init__(self,url=None,useProxy=False):
        self.IPproxy=None
        self.useIPproxy=useProxy

        self.client=pymongo.MongoClient('localhost',27017)
        self.COL=self.client['WeiboLogin']
        self.cookiewithoutDOC=self.COL['CookieWithoutLogin']


        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',charset='utf8')
        self.cursor=self.connect.cursor()

        # self.COL = self.client['WeiboLogin']
        self.cookieDOC = self.COL['cookieDoc']
        self.proxyCOL = self.client['IpProxy2']
        self.proxyDOC = self.proxyCOL['weiboDOC']


        self.proxyIPport=None
        self.proxytype='Https'
        self.proxyIP = None
        self.purpose = None
        self.proxyhandler = None

        self.url=url
        self.header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.cookie=cookielib.LWPCookieJar()
        self.cookieHandler=None
        self.openner=None


        self.request=None
        self.response=None

    def enableCookie(self,purpose=None):#default来表示默认的用途,就是随便使用,若是想制定爬去某个层次的内容的话,在default里边支出

        self.purpose=purpose
        requestsproxy=None
        if self.useIPproxy:
            proxylist=[]
            for i in self.proxyDOC.find_one({'used':False},{'_id':0}):
                proxylist.append({
                    'ip':i['ip'],
                    'port':i['port'],
                    'proxytype':i['proxytype']
                })

            proxyinthis=proxylist.pop()
            self.proxyDOC.update({'ip':proxyinthis['ip']},{'$set':{'used':True}})

            self.proxyIP=proxyinthis['ip']#之所以把它写到self里,因为外边调用后如果成功了,会将self中的内容写到数据库中.
            self.proxyIPport=proxyinthis['port']
            self.proxytype=proxyinthis['proxytype']

            # self.proxyIP='122.70.141.42'
            # self.proxyIPport='80'
            # self.proxytype='https'

            print '-----------'+self.proxyIP+':'+self.proxyIPport


            self.cookie=cookielib.LWPCookieJar()
            self.cookieHandler=urllib2.HTTPCookieProcessor(self.cookie)

            self.proxyhandler = urllib2.ProxyHandler({proxyinthis['proxytype']: proxyinthis['proxytype']+'://%s:%s' % (self.proxyIP, self.proxyIPport)})
            self.openner = urllib2.build_opener(self.cookieHandler, self.proxyhandler)
            # proxy_support=urllib2.ProxyHandler({'http':'http://115.85.233.94:80'})
            # self.openner=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler,proxy_support)
        else:
            self.cookieHandler=urllib2.HTTPCookieProcessor(self.cookie)
            self.openner=urllib2.build_opener(self.cookieHandler)#5-19去掉了,urllib2.HttpHandler
        # urllib2.install_opener(openner)
        # urllib2.install_opener(openner)


        #需要在这里检查一下代理ip是否可用,如果可用再返回,不管用没用代理,这里都可以,如果没用太低的话,delete就会删除不了东西.

        try:
            self.run()
        except Exception as e:
            print e
            self.proxyDOC.update({'ip': self.proxyIP},{'$set':{'drop':'can not use'}},upsert=True)
            self.enableCookie()

        # requestsproxy=urllib2.Request(url='http://login.sina.com.cn/crossdomain2.php?action=login',headers=self.header)
        # data=self.openner.open(requestsproxy).read()
        # if len(data)>100:
        #     pass
        # else:#如果这个代理ip不能用,先从数据库中删除,之后再来一次
        #     self.proxyDOC.delete_one({'ip':self.proxyIP})
        #     self.enableCookie()

        return self



    def urlget(self):
        for i in self.DOC.find({},{'_id':0,'forum_url':1}).limit(10):
            yield i['forum_url']
            # self.DOC.update({'forum_url':i['forum_url']},{'dealed':True},upsert=True)

    def run(self):


        url_visiter_visiter1='https://passport.weibo.com/visitor/visitor?a=incarnate&t='
        beforeurllist=[
            'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)',
            'http://login.sina.com.cn/crossdomain2.php?action=login',
            'http://i.sso.sina.com.cn/js/ssologin.js',
            # 'https://login.sina.com.cn/cgi/pin.php',
            'http://weibo.com/login.php',
            'https://passport.weibo.com/visitor/visitor',
            'http://weibo.com/aj/v6/top/topnavthird',
            'https://passport.weibo.com/visitor/visitor?a=incarnate&t=VIPZmdsCw%2BQyrNnxcNovFvODkEmJ5oUDUTdByeL5Pco%3D&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand=0.10277698794252332',#这里边的有些东西是可以换的095不可以换,但是之前的貌似可以
            'https://login.sina.com.cn/visitor/visitor?a=crossdomain&cb=return_back&s=_2AkMue28jf8NxqwJRmP8dyGngZIhxyw_EieKYJ574JRMxHRl-yT83qnFftRAkUXaBBP2h00j10Z7Ne2xSYkQMEg..&sp=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W555Mkrw4C8Pv59U1xT0MxL&from=weibo&_rand=0.2432791179006497',
            'http://weibo.com',
            'https://login.sina.com.cn/',
        ]
        for i in beforeurllist:
            request=urllib2.Request(url=i,headers=self.header)
            data=self.openner.open(request,timeout=5000)
            print data.url
            print data.headers
            time.sleep(0.1)

        print self.cookie
        cookiedictwithoutlogin={}
        try:
            for i in self.cookie:
                cookiedictwithoutlogin[i['name']]=i['value']
                # self.cookiewithoutDOC.insert({i['name']:i['value']})
            # self.cookiewithoutDOC.insert({'tid':'VIPZmdsCw+QyrNnxcNovFvODkEmJ5oUDUTdByeL5Pco=__095'})
            # self.cookiewithoutDOC.insert({'proxyIP':self.proxyIP})
            # self.cookiewithoutDOC.insert({'proxyIPport':self.proxyIPport})
            # self.cookiewithoutDOC.insert({'proxytype':self.proxytype})
            cookiedictwithoutlogin['tid']='VIPZmdsCw+QyrNnxcNovFvODkEmJ5oUDUTdByeL5Pco=__095'
            cookiedictwithoutlogin['proxyIP']=self.proxyIP
            cookiedictwithoutlogin['proxyIPport']=self.proxyIPport
            cookiedictwithoutlogin['proxytype']=self.proxytype
            self.cookiewithoutDOC.insert(cookiedictwithoutlogin)
        except Exception as e:
            print e#153.101.205.25:3128--------203.110.170.50:80



        # for i in self.urlget():
        #     redict_url=''
        #     while 'http://weibo.com/1258954655/F3EDzbEyh' not in redict_url:
        #         self.request=urllib2.Request(url=i,headers=self.header)
        #         data=self.openner.open(self.request)
        #         print data.url
        #         redict_url=data.url
        #         datasoup=BeautifulSoup(data.read(),'lxml')
        #         print datasoup
        #         time.sleep(5)

        # response=self.openner.open(self.request)
        # data=response.read()
        # datasoup=BeautifulSoup(data,'lxml')




class CookieGet2:
    def __init__(self):
        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',charset='utf8')
        self.cursor=self.connect.cursor()

        self.headers={
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
            # 'cookie':'login_sid_t=aa544db4f87986a0a38f267cead3c787; _s_tentry=-; Apache=7523975442007.387.1497494316556; SINAGLOBAL=7523975442007.387.1497494316556; ULV=1497494316560:1:1:1:7523975442007.387.1497494316556:; SUB=_2AkMuHXwCf8NxqwJRmP4XxG7maIhzyAzEieKYQY3ZJRMxHRl-yT83qhNTtRCl4TR4Z99V0GM3KtjTss_8evN6_w..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWLphwKCinbC-wHgV-iMLQs',
            'referer':'https://m.weibo.cn/status/EslDScVTn?luicode=20000061&lfid=4118572374788617&featurecode=20000180',
            'cookie':'_T_WM=aeee6a0b8b3b11ce4dad79442fcacdc0; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D4067563803082477%26luicode%3D10000011%26lfid%3D1005055526045431'
        }

    def getZhuanFa(self,urlZhuanfa,proxyInGetZhuanFa):
        print  urlZhuanfa#不要再忘了爬了多少页了
        # print 'sb'

        cookie2 = cookielib.LWPCookieJar()
        session2 = requests.session()
        session2.headers = self.headers
        session2.cookies=cookie2

        connectZhuanFa = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', charset='utf8')
        cursor = connectZhuanFa.cursor()




        # connectZhuanFa=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',charset='utf8')
        # cursor=connectZhuanFa.cursor()

        # response1 = session1.request(method='GET', url=urlZhuanfa)
        # datasoup = BeautifulSoup(response1.text, 'lxml')

##################3begain
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'cookie': '_2AkMuHsoHf8NxqwJRmPAVz2rrb4l0wg_EieKYQjvcJRMxHRl-yT83qmEttRC2H92yTTybryMKqufA-zBjgQfOFQ..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhQryML1A3cQ0ff0o_nA699; ULV=1497523040669:2:2:2:5981387526256.865.1497523040649:1497515307709; login_sid_t=093c4734440ff8854fdd5df2aa5cba37; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; YF-V5-G0=b8115b96b42d4782ab3a2201c5eba25d; WBStorage=5ea47215d42b077f|undefined; _s_tentry=-; Apache=5981387526256.865.1497523040649; YF-Page-G0=f017d20b1081f0a1606831bba19e407b'

        }
        headers2={
            'cookie': '_2AkMuHsoHf8NxqwJRmPAVz2rrb4l0wg_EieKYQjvcJRMxHRl-yT83qmEttRC2H92yTTybryMKqufA-zBjgQfOFQ..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhQryML1A3cQ0ff0o_nA699; ULV=1497523040669:2:2:2:5981387526256.865.1497523040649:1497515307709; login_sid_t=093c4734440ff8854fdd5df2aa5cba37; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; YF-V5-G0=b8115b96b42d4782ab3a2201c5eba25d; WBStorage=5ea47215d42b077f|undefined; _s_tentry=-; Apache=5981387526256.865.1497523040649; YF-Page-G0=f017d20b1081f0a1606831bba19e407b',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        if len(proxyWouldChange)>3:
            session2.headers=headers1
            session2.cookies=proxyWouldChange[random.randint(0,len(proxyWouldChange)-1)]
        else:
            session2.headers=headers2
        urlsss = urlZhuanfa

        session2.proxies=proxyInGetZhuanFa

        try:
            response2 = session2.request(method='GET', url=urlsss)
            datajson = json.loads(response2.text)
            proxyWouldChange.add(response2.cookies)
        except Exception as e:
            print e
            return
        for json1 in datajson['data']:
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
            # yield [id,text,raw_text,created_at,userid,userscreen_name,userprofile_url,userverified,userverified_type]
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

        proxyInUsing.remove(proxyInGetZhuanFa)
        time.sleep(random.randint(1, 4))


    def textduoxiancheng(self,sb,sq):
        print sb
        print sq



    def run(self,url1,limit1=1,limit2=2):
        cookie1=cookielib.LWPCookieJar()
        session1=requests.session()
        session1.headers=self.headers
        session1.cookies=cookie1


        for url11 in url1:
            response1=session1.request(method='GET',url=url11)
            # datasoup=BeautifulSoup(response1.text,'lxml')
            # print '\n\n\n-----------------------------------'
            # print response1.headers['Set-Cookie']

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
            while len(threadlist)< 10 and urllist:
                thisurl=urllist.pop()
                while proxyrandom is None or proxyrandom in proxyInUsing:
                    proxyrandom = proxylist[random.randint(0, len(proxylist)-1)]
                proxyInUsing.append(proxyrandom)
                thread2=threading.Thread(target=self.getZhuanFa,args=(thisurl,proxyrandom))

                thread2.setDaemon(True)

                thread2.start()
                # thread2.run()
                threadlist.append(thread2)
                print len(threadlist)
            time.sleep(5)


        # for pagenum in range(807,10000):
        #     urlsss='https://m.weibo.cn/api/statuses/repostTimeline?id=4067563803082477&page='+str(pagenum)
        #
        #
        #     resultlist=self.getZhuanFa(urlZhuanfa=urlsss)

            #限速模块去掉
            # print '----------pagenum------'+urlsss
            # for infozhuanfa in resultlist:
            #     print infozhuanfa
            # sleepnum=random.randint(1,5)
            # if sleepnum>4:
            #     configurl='https://m.weibo.cn/api/config'
            #     referer='https://m.weibo.cn/status/EslDScVTn?luicode=20000061&lfid=4118572374788617&featurecode=20000180'
            #     session1.headers['referer']=referer
            #     session1.request(method='GET',url=configurl)
            #     time.sleep(sleepnum+6)
            # else:
            #     time.sleep(sleepnum)




    def yiedlurl(self):
        urllistall=[]
        for pagenum in range(limitDown, limitUP):
            urlsss = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4067563803082477&page=' + str(pagenum)
            # yield urlsss
            urllistall.append(urlsss)
        return urllistall





# def runfunction(num):
#     print num
#     thisclass = CookieGetWithoutLogin(useProxy=True)
#     thisclass.enableCookie()




if __name__ == '__main__':
    thisclass=CookieGet2()
    lsit1=[
        'http://m.weibo.cn/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom&filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment&jumpfrom=weibocom&filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/status/ED9oalVvo',
        'http://weibo.com/5526045431/ED9oalVvo?filter=hot&root_comment_id=0&type=comment',
        'https://m.weibo.cn/statuses/extend?id=4093308865225942',
        'https://m.weibo.cn/api/comments/show?id=4093308865225942&page=1',
        'https://m.weibo.cn/api/config',

    ]
    thisclass.run(lsit1)


    # urllist=thisclass.yiedlurl()
    # pool1=pool.Pool(processes=4)
    # pool1.map(thisclass.getZhuanFa,urllist)
    # pool1.close()
    # pool1.join()
