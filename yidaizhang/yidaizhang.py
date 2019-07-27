import requests
import json
import re
import urllib
import PyPDF2,os
import time
from tkinter import *
import tkinter.messagebox
request=requests.session()
#————————————————————————————————
#设置年份、月份：

root=Tk()
root.title('易代账爬虫程序')

root.iconbitmap('D:/pachong/yidaizhang/bitbug_favicon.ico')
root.geometry("280x540")
Label(root,text='——————————+——————————',bg='#7FFFD4').grid(row=0,column=0,columnspan=2)
Label(root,text='年份：').grid(row=1,column=0,sticky=E)
Label(root,text='公司名称：').grid(row=2,column=0,sticky=E)
Label(root,text='cookies:',font='微软雅黑',fg='green').grid(row=7,column=0)
Label(root,text='CIC：').grid(row=8,column=0,sticky=E)
Label(root,text='PHPSESSID_EE：').grid(row=9,column=0,sticky=E)

Label(root,text='起始月份:').grid(row=15,column=0,sticky=E)
Label(root,text='截至月份:').grid(row=16,column=0,sticky=E)

m1=Entry(root)
m1.insert(END, '1')
m2=Entry(root)
m2.insert(END, '12')

m1.grid(row=15,column=1,sticky=W)
m2.grid(row=16,column=1,sticky=W)

e1=Entry(root)
e1.insert(END, '2017')
e2=Entry(root)


e1.grid(row=1,column=1,sticky=W)
e2.grid(row=2,column=1,sticky=W)


c1=Entry(root)
c1.grid(row=8,column=1,sticky=W)
c2=Entry(root)
c2.grid(row=9,column=1,sticky=W)
#——————————————star
def start():
    year =int(e1.get())
    mon1=int(m1.get())
    mon2=int(m2.get())
    key1 =str(e2.get())
    #————————————————————————————————
    cictxt = c1.get()
    eextx=c2.get()

    filetxt = 'D:/pachong/易代账cookies.txt'

    if len(cictxt) > 3 and len(eextx)>3:
        cookies='CIC='+str(cictxt)+';PHPSESSID_EE='+str(eextx)+';'

        p = open(filetxt, 'wb')
        new_txt = cookies.encode('utf-8')
        p.write(new_txt)
        p.close()

    #————————————————————————————————登陆cookis   《主页的bookrecordlogin获取》
    #def getTXT
    file=filetxt
    txtp=open(file,'rb')
    strline=str(txtp.read()).replace(' ','').replace('b\'','')

    PHPSESSID_EEr=r'PHPSESSID_EE=(.*?);'
    PHPSESSID_EE=re.findall(PHPSESSID_EEr,strline)[0]
    CICr=r'CIC=(.*?);'
    CIC=re.findall(CICr,strline)[0]
    txtp.close()
    #def getTXT

    cookielogin='PHPSESSID_EE='+PHPSESSID_EE+';CIC='+CIC
    cookieslogin = {i.split('=')[0]: i.split('=')[1] for i in cookielogin.split(';')}  # ——cookies切片
    #————————————————————————————————登陆cookis


    time_start=time.time()

    mkpath = r"D:/pachong/账无忧、易代账/易代账/结果/%s"%key1

    def mkdir(path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False
    # 调用函数
    mkdir(mkpath)

    def search(key1):#——————————查找公司，返回第一家的userid(用于获取账簿码tcode)、id(账簿号。拼接pdf地址)  name——userid，id

        # key ='华夏富商（北京）科技有限公司'
        key= urllib.parse.quote(key1)
        url='http://e.chanjet.com/api/v1/account/page?start=0&limit=100&conds=%7B%22is_owner%22%3A0%2C%22name%22%3A%22'+key+'%22%2C%22acc_number%22%3A%22%'+key+'%22%7D&page=0&isRecycle=0'
        keyPage=requests.get(url,cookies=cookieslogin)
        # print(keyPage.content)


        r=r'"book_id":(.*?),'
        abookNum=str(re.findall(r, str(keyPage.content))[0])
        dic = json.loads(keyPage.content)
        name=dic['data']['list'][0]['name']
        print('公司全称：',name)

        user_id=dic['data']['list'][0]['user_id']
        return user_id,abookNum
    searchResult=search(key1)
    user_id=searchResult[0]#————————————————user_id
    abookNum=searchResult[1]#———————————————账簿号abookNum
    #——————————————————————————登陆cookis
    #——————————————————————————传入（userid），获取账簿码（tcode）   userid——tcode
    def gettCode(user_id):
        url='http://e.chanjet.com/api/v1/app/state?&user_id=%s'%user_id
        newUrl=requests.get(url,cookies=cookieslogin)
        # print(newUrl.text)
        r=r'"url":"http:\\/\\/(.*?)\\'
        url2=re.findall(r,newUrl.text)
        tCode=str(url2).strip('[]\'')
        return tCode
    tCode=gettCode(user_id)

    header={
    'Accept':'application/javascript, application/json',
    'Accept-Encoding':'gzip, deflate, sdch',

    'Content-Type':'application/json',
    # Cookie:JSESSIONID=0D0E6DB67CF1CF8EBDD3ACB7463DFE42; sajssdk_2015_cross_new_user=1; acw_tc=AQAAACTgKTp3DQQATSJK365VO07MeJND; __VCAP_ID__=5c0e616ae68b58d175f512ac77c41e00f82bffda6c862f1607be2f9503367f88; gr_user_id=23d74db5-a6ee-45dc-94cc-6357e54c8405; gr_session_id_84e72a3b0e1fca44=08be52e1-9bfb-4612-96d6-34213604d842; gr_cs1_08be52e1-9bfb-4612-96d6-34213604d842=vmDomain%3Au1sqzpri0kte; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22164b6377fa33f-00a6c9add84349-5d4e211f-1024000-164b6377fa411f%22%2C%22%24device_id%22%3A%22164b6377fa33f-00a6c9add84349-5d4e211f-1024000-164b6377fa411f%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; gr_session_id_84e72a3b0e1fca44_08be52e1-9bfb-4612-96d6-34213604d842=true
    'DNT':'1',
    'Host':'u6f3xmbbkki4.chanapp.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://u6f3xmbbkki4.chanapp.com/chanjet/finance/index.html?1532138784',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}
    #——————————————————————————获取cookies里的会话ID（JSESSIONID）(从返回的cookies里获取)
    def getJSESSIONID(tcode):
        urlJSESSIONID='http://'+str(tcode)+'.chanapp.com/chanjet/finance/restlet/v2/web/profile/GetInfo?'
        jsessionidPage= requests.get(urlJSESSIONID, headers=header,cookies=cookieslogin)
        # print(jsessionidPage.cookies)
        r=r'JSESSIONID=(.*?)for'
        jsessionid=str(re.findall(r,str(jsessionidPage.cookies))).strip('[]\'\s*')
        # print('Get JSESSIONID成功！ JSESSIONID是%s'%jsessionid)

        return jsessionid
    jsessionid=getJSESSIONID(tCode)

    #——————————————————————————获取code来激活会话ID（JSESSIONID）  <<这里有CIC cookies>>《https://cia.chanapp.chanjet.com/internal_api/authorizeByJsonp?client_id=finance&state=xxsss&callback=dojo_request_script_callbacks.dojo_request_script0》
    def getCode():
       #专属cookies
        codecookie = 'CIC='+CIC+'; BIGDATAID=rBAmAltR+vuI/j4zAw8oAg=='# sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22164b83cb9a9101-07f4f6f7040cf6-5d4e211f-1024000-164b83cb9ab2d%22%2C%22%24device_id%22%3A%22164b83cb9a9101-07f4f6f7040cf6-5d4e211f-1024000-164b83cb9ab2d%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D'
        codecookies = {i.split('=')[0]: i.split('=')[1] for i in codecookie.split(';')}  # ——cookies切片

        urlgetCode = 'https://cia.chanapp.chanjet.com/internal_api/authorizeByJsonp?client_id=finance&state=xxsss&callback=dojo_request_script_callbacks.dojo_request_script0'
        getCode=requests.get(urlgetCode,cookies=codecookies)
        r=r'"code":"(.*?)"'
        code=str(re.findall(r,str(getCode.text))).strip('[]\'')

        # print('Get code 成功！codes是：'+str(code).strip('[]\''))
        return code
    code=getCode()

    #——————————————————————————激活会话id（JSESSIONID）
    def session(jsessionid,tcode,code):
        # 需要激活的cookies（JSESSIONID）
        codecookie = 'JSESSIONID='+str(jsessionid)+'; __VCAP_ID__=4f5b57a7e6599a986a94f140ef29922f70353c02bd973fefc61cc4facfd447cb '
        codecookies = {i.split('=')[0]: i.split('=')[1] for i in codecookie.split(';')}  # ——cookies切片

        urlsession='http://'+str(tcode)+'/chanjet/finance/services/1.0/user/session?code='+str(code)
        session=requests.get(urlsession,cookies=codecookies)
        # print(codecookie,urlsession)
        # print(session.text)
        sessiondic=json.loads(session.content)
        jsessionidreal=sessiondic['id']



        if 'id' in session.text:
            print('进入网站成功！')
            print('开始获取数据.......耐心点，比较慢。')
            # print(jsessionidreal)
        return jsessionidreal
    jsessionidreal=session(jsessionid,tCode,code)

    #——————————————————————————构造获取pdf所认证的ccodecookie
    codecookie = 'JSESSIONID=' + str(jsessionidreal) + '; __VCAP_ID__=4f5b57a7e6599a986a94f140ef29922f70353c02bd973fefc61cc4facfd447cb '
    codecookies = {i.split('=')[0]: i.split('=')[1] for i in codecookie.split(';')}  # ——cookies切片
    #——————————————————————————获取资产负债表
    def getalancesheet():
        pdfwriter = PyPDF2.PdfFileWriter()
        for i in range(mon1, mon2 + 1):
            if i<10:
                o='0'+str(i)
            else :
                o=str(i)
            url='http://'+tCode+'/chanjet/finance/restlet/v2/web/balancesheet/Pdf?ACCOUNTBOOK='+str(abookNum)+'&queryCond=%7B%22period%22%3A%20%22'+str(year)+''+o+'%22%2C%20%22orign%22%3A%20false%7D&'
            # print(url)
            # print(codecookie)
            pdf=requests.get(url,cookies=codecookies)

            r=r'"resultObj"\s*:\s*"(.*?)"'
            site=re.findall(r,str(pdf.content))
            # print(site)
            url1=site[0]#——————————————————拿到pdf地址(要素：报表地址+正确的cookies)
            pdfreal = requests.get(url1, cookies=codecookies)

            file = "D:\\pachong\\账无忧、易代账\\易代账\\本次资产负债表\\资产负债表" + str(i) + "月.pdf"
            fp = open(file, "w+b")  # 打开一个文本文件
            fp.write(pdfreal.content)  # 写入数据i
            fp.close()  # 关闭文件.#抓取资产负债表（1-12月）


            # ——————建立pdfreader，先读出来，放在pdfreader里，方便后续操作。。
            readFile = file

            pdfreader = PyPDF2.PdfFileReader(readFile)

            page1 = pdfreader.getPage(0)
            # ——————建立pdfwriter，先写进到writer里（可以add多页），再导入目标文件。

            # ——————add多个页面到writer

            pdfwriter.addPage(page1)

        print('获取资产负债表成功！')
        return pdfwriter
    pdfwriter=getalancesheet()

    #——————————————————————————获取利润表
    def getIcomereport():
        for i in range(mon1, mon2 + 1):
            if i<10:
                o='0'+str(i)
            else :
                o=str(i)
            url='http://'+tCode+'/chanjet/finance/restlet/v2/web/incomereport/Pdf?ACCOUNTBOOK='+str(abookNum)+'&queryCond=%7B%22period%22%3A%20%22'+str(year)+''+o+'%22%7D&_'
            pdf = requests.get(url, cookies=codecookies)

            r = r'"resultObj"\s*:\s*"(.*?)"'
            site = re.findall(r, str(pdf.content))
            # print(site)
            url1 = site[0]  # ——————————————————拿到pdf地址(要素：报表地址+正确的cookies)
            pdfreal = requests.get(url1, cookies=codecookies)
            file = "D:/pachong/账无忧、易代账/易代账/本次利润表/" + str(i) + "月.pdf"
            fp = open(file, "w+b")  # 打开一个文本文件
            fp.write(pdfreal.content)  # 写入数据i
            fp.close()  # 关闭文件.#抓取利润表（1-12月）


            # ——————建立pdfreader，先读出来，放在pdfreader里，方便后续操作。。
            readFile = file
            pdfreader = PyPDF2.PdfFileReader(readFile)
            page1 = pdfreader.getPage(0)

            # ——————add多个页面到writer
            pdfwriter.addPage(page1)
        # ——————writer导入目标文件
        outFile = mkpath
        p = open(outFile+ "\\资产负债表和利润表.pdf", "w+b")  # 打开一个文本文件
        p.close()  # 关闭文件.#抓取利润表表（1-12月）

        pdfwriter.write(open(outFile+ "\\资产负债表和利润表.pdf", 'wb'))






        print('获取利润表成功！')
    getIcomereport()
    #——————————————————————————获取总账
    def getotalAccount():
        url='http://'+tCode+'/chanjet/finance/restlet/v2/web/report/Down?type=YEARACCOUNT&queryCond={%22bookId%22:%22'+str(abookNum)+'%22,%20%22type%22:%20%22totalAccount%22,%22year%22:%20%22'+str(year)+'%22,%20%22pdfOrExcel%22:%22pdf%22}'



        pdfreal = requests.get(url, cookies=codecookies)
        fp = open(mkpath + "\\总账.pdf", "w+b")  # 打开一个文本文件
        fp.write(pdfreal.content)  # 写入数据i
        fp.close()  # 关闭文件
        # ————————数总账
        readFile = mkpath + "\\总账.pdf"
        pdfreader = PyPDF2.PdfFileReader(readFile)
        nums = pdfreader.getNumPages()
        os.rename(mkpath + "\\总账.pdf", mkpath + "\\总账%s页.pdf" % nums)

        print('获取总账成功！共%s页'% nums)
    getotalAccount()
    #——————————————————————————获取明细账
    def getDetailAccount():
        if mon1<10:
            o='0'+str(mon1)
        else:
            o=str(mon1)
        if mon2 < 10:
            p= '0' + str(mon2)
        else:
            p= str(mon2)
        url='http://'+tCode+'/chanjet/finance/restlet/v2/web/report/Down?type=YEARACCOUNT&queryCond={%22bookId%22:%22'+str(abookNum)+'%22,%20%22type%22:%20%22detailAccount%22,%22year%22:%20%22'+str(year)+''+o+'-'+str(year)+''+p+'%22,%20%22pdfOrExcel%22:%22pdf%22}'
        pdfreal = requests.get(url, cookies=codecookies)
        fp = open(mkpath + "\\明细账.pdf", "w+b")  # 打开一个文本文件
        fp.write(pdfreal.content)  # 写入数据i
        fp.close()  # 关闭文件
        # ————数明细账
        readFile = mkpath + "\\明细账.pdf"
        pdfreader = PyPDF2.PdfFileReader(readFile)
        nums = pdfreader.getNumPages()

        os.rename(mkpath + "\\明细账.pdf", mkpath + "\\明细账 %s页.pdf" % nums)
        print('获取明细账成功！共%s页'%nums)
    getDetailAccount()
    #——————————————————————————获取凭证
    #——————————————————————————获取凭证列表
    def getVocherlist():
        url='http://'+tCode+'/chanjet/finance/restlet/v2/web/voucher/VoucherList?ACCOUNTBOOK='+str(abookNum)
        idlist=[]
        for i in range(mon1, mon2 + 1):
            if i<10:
                o='0'+str(i)
            else :
                o=str(i)
            data={'pageCount':1,
                    'pageSize':"50",
                    'period':str(year)+o,
                    'text':""}
            vocherlist= requests.post(url,data=data, cookies=codecookies)
            r=r'"generatedBy"\s:\s.*?,\\n\s*"id"\s:\s(.*?),\\n\s*"auditStatus"'
            getidlist=re.findall(r,str(vocherlist.content))
            idlist.extend(getidlist)

        idList=str(idlist).strip('[]\'').replace('\', \'',',')
        # print(idList)
        return idList
            # print(str(vocherlist.content))
    idList=getVocherlist()
    #——————————————————————————下载凭证列表
    def getVocher():
        url='http://'+tCode+'/chanjet/finance/restlet/v2/web/voucher/PrintVoucher?ACCOUNTBOOK='+str(abookNum)
        data={'printCount':"-1",
                'printStyle':"0",
             'voucherIds':idList}
        pdf = requests.post(url,data=data, cookies=codecookies)
        r = r'"resultObj"\s*:\s*"(.*?)"'
        site = re.findall(r, str(pdf.content))
        # print(site)
        url1 = site[0]  # ——————————————————拿到pdf地址(要素：报表地址+正确的cookies)
        pdfreal = requests.get(url1, cookies=codecookies)
        fp = open(mkpath + "\\凭证.pdf", "w+b")  # 打开一个文本文件
        fp.write(pdfreal.content)  # 写入数据i
        fp.close()  # 关闭文件.#抓取利润表（1-12月）
        print('获取凭证成功！')
    getVocher()
    time_end=time.time()
    print('全部抓取完成！共耗时：',round(time_end-time_start,1),"秒。"  )

    tkinter.messagebox.showinfo("获取结果", "全部获取成功!" )

Button(root,text='开始',command=start, width=30, height=2).grid(row=5,column=0,columnspan=2,padx=30,pady=5)
Button(root,text='退出',width=30, height=2,command=root.quit).grid(row=6,column=0,columnspan=2,padx=10,pady=5)
photo = PhotoImage(file="D:/pachong/yidaizhang/tupian.png")#file：t图片路径
imgLabel = Label(root,image=photo)
imgLabel.grid(row=10,column=0,rowspan=2,columnspan=2,padx=1,pady=1)

mainloop()

