import requests
import urllib.request
request = requests.Session()
import re
import os
import PyPDF2
import time
from tkinter import *
import tkinter.messagebox
#def getTXT():

root=Tk()
root.title('账无忧爬虫程序')
# root.overrideredirect(1)
#设置窗口图标



root.iconbitmap('D:/pachong/bitbug_favicon.ico')
root.geometry("280x380")

Label(root,text='年份：').grid(row=1,column=0)
Label(root,text='公司名称：').grid(row=2,column=0)
Label(root,text='cookies:').grid(row=7,column=0)
Label(root,text='起始月份:').grid(row=15,column=0,sticky=E)
Label(root,text='截至月份:').grid(row=16,column=0,sticky=E)

#——————————复选框




m1=Entry(root)
m1.insert(END, '1')
m2=Entry(root)
m2.insert(END, '12')

m1.grid(row=15,column=1,sticky=W)
m2.grid(row=16,column=1,sticky=W)




e1=Entry(root)
e1.insert(END, '2017')
e2=Entry(root)
e3=Entry(root)

e1.grid(row=1,column=1)
e2.grid(row=2,column=1)
e3.grid(row=7,column=1)

def start():
    mon1 = int(m1.get())
    mon2 = int(m2.get())
    txt=e3.get()
    filetxt='D:/pachong/账无忧cookies.txt'

    if len(txt)>3:
        p=open(filetxt,'wb')
        new_txt=txt.encode('utf-8')
        p.write(new_txt)
        p.close()
        

    txtp=open(filetxt,'rb')

    strline=str(txtp.read()).replace('\\xa3\\xba','').replace(' ','').replace('b\'','')

    SessionIdr=r'ASP.NET_SessionId=(.*?);'
    SessionId=re.findall(SessionIdr,strline)[0]

    zwyClientr=r'zwyClient=(.*?);'
    zwyClient=re.findall(zwyClientr,strline)[0]

    fctr=r'fct=(.*?);'
    fct=re.findall(fctr,strline)[0]

    JSESSIONIDr=r'JSESSIONID=(.*?);'
    JSESSIONID=re.findall(JSESSIONIDr,strline)[0]

    txtp.close()
    #就把复制来的cookies替换下面的                                                                                                               |
    # cookie='zwyClient=324e1999-5271-4271-a668-c4c686af276a; JSESSIONID=ACFF59F9755935C7FF6209B1C3B2B697; ASP.NET_SessionId=wchromivvt5fj2amn4gzro12; gj-phone=13680010837; fct=1523522038c1c9afa5a48a6aaaeaf951; fc-phone=13680010837; Hm_lvt_794b82ea3952be1eb6ae7e29afa0d21c=1532753482,1532754821,1532754907,1532760369; Hm_lpvt_794b82ea3952be1eb6ae7e29afa0d21c=1532760369; Hm_lvt_582fb6e62a4f0607ad9f32dafa4efebe=1532753483,1532754821,1532754907,1532760369; Hm_lpvt_582fb6e62a4f0607ad9f32dafa4efebe=1532760369; currentli=0; currentpage=PersonalIndex.aspx'
    cookie='ASP.NET_SessionId='+SessionId+'; zwyClient='+zwyClient+'; fct='+fct+'; fc-phone=13680010837; JSESSIONID='+JSESSIONID
    # print(cookie)
    cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie.split(';')}  # ——cookies切片
    #——————————————————————————————年、月设置

    
    year = e1.get()
    s = e2.get()
    


    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Cache - Control': 'max - age = 0',
                  'Content - Length': '1057',
                  'Content - Type': 'application / x - www - form - urlencoded',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Content-Length': '0', 'DNT': '1',
                  'Host': 'vip2.kdzwy.com:81',
                  'Origin': 'http://vip2.kdzwy.com:81',
                  'Referer': 'http://vip2.kdzwy.com:81/print/print-settings-voucher.jsp?type=7&id=5',
                  'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                  'X - Requested - With': 'XMLHttpRequest',
                  'Upgrade - Insecure - Requests': '1'}

    # ——————————————————————————————建文件夹
    time_start = time.time()

    mkpath = r"D:/pachong/账无忧、易代账/账无忧/结果/%s" % s

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

    def search():
        key = urllib.parse.quote(s)
        url = 'http://vip2.kdzwy.com/dzgjvip2/Acct/Ashx/CustomerListAsSimple.ashx?dataType=emp&deptid=2043530000005981&empid=2043530000018073&deptName=%E6%B7%B1%E5%9C%B3%E7%91%9E%E5%8D%9A%E4%BC%9A%E8%AE%A1%E5%B8%88%E4%BA%8B%E5%8A%A1%E6%89%80&pageIndex=0&pageSize=10&searchText=' + str(
            key) + '&version=1532228249530&roletype=customer&formmode=0&feeStatus=0&service_id=5&opetype=0&waitdispatch=0&taxtype=0'
        data = {'dataType': 'emp',
                'deptid': 2043530000005981,
                'empid': 2043530000018073,
                'deptName': '深圳瑞博会计师事务所',
                'pageIndex': 0,
                'pageSize': 10,
                'searchText': s,
                'version': 1532228249530,
                'roletype': 'customer',
                'formmode': 0,
                'feeStatus': 0,
                'service_id': 5,
                'opetype': 0,
                }
        result = requests.post(url, data=data, cookies=cookies)
        r = r'href=\s*\'(.*?)助理会计'
        comid = re.findall(r, str(result.text))
        namer = r'id=\'checkbox2\'\s*buname=\'(.*?)\''
        name = str(re.findall(namer, str(result.text))).strip('[]\'')
        Buidsurl = str(comid[0]).strip('[]\'') + '%E5%8A%A9%E7%90%86%E4%BC%9A%E8%AE%A1'
        # print(Buidsurl,str(result.text))
        print('查找成功！\n公司全称是：%s' % name)
        return Buidsurl, name
    rearchR=search()
    Buidsurl = rearchR[0]
    name = rearchR[1]
    # ——————————————————————————————切参数
    siIdr = r'siId=(.*?)&'
    siId = str(re.findall(siIdr, Buidsurl)).strip('[]\'')
    companycoidr = r'companycoid=(.*?)&'
    companycoid = str(re.findall(companycoidr, Buidsurl)).strip('[]\'')
    buidr = r'buid=(.*?)&'
    buid = str(re.findall(buidr, Buidsurl)).strip('[]\'')
    orderIdr = r'orderId=(.*?)&'
    orderId = str(re.findall(orderIdr, Buidsurl)).strip('[]\'')
    zwycompIdr = r'zwycompId=(.*?)&'
    zwycompId = str(re.findall(zwycompIdr, Buidsurl)).strip('[]\'')

    # ——————————————————————————————切参数
    # —————————进入页面
    def enter():
        url = Buidsurl
        data = {'siId': siId,
                'companycoid': companycoid,
                'language': 'zh-CHS',
                'buid': buid,
                'dataType': 'emp',
                'deptid': 2043530000005981,
                'empid': 2043530000018073,
                'deptlevel': '',
                'name': name,
                'logonName': 13680010837,
                'site': 'NULL',
                'businesstype': 0,
                'CompanyScale': 0,
                'orderId': orderId,
                'zwycompId': zwycompId,
                'tax': 'Small',
                'username': '助理会计',
                'displayUserPY': 'false'
                }
        backout = requests.post(url, data=data, cookies=cookies)

        if '200' in str(backout):
            print('进入页面成功！请耐心等待。。。。%s' % backout)
        else:
            print('进入页面失败！%s' % backout)
    enter()

    # —————————进入页面

    # ————资产负债表
    def tableBalance1():
        pdfwriter = PyPDF2.PdfFileWriter()
        for i in range(mon1, mon2 + 1):
            url = 'http://vip2.kdzwy.com:81/report/report?m=printBalance&reporttype=balance'
            data = {'dataField': 'name_0#rownum_0#balance_0#prebalance_0#name_1#rownum_1#balance_1#prebalance_1',
                    'columnTitle': '%E8%B5%84%E4%BA%A7#%E8%A1%8C%E6%AC%A1#%E6%9C%9F%E6%9C%AB%E6%95%B0#%E5%B9%B4%E5%88%9D%E6%95%B0#%E8%B4%9F%E5%80%BA%E5%92%8C%E6%89%80%E6%9C%89%E8%80%85%EF%BC%88%E6%88%96%E8%82%A1%E4%B8%9C%EF%BC%89%E6%9D%83%E7%9B%8A#%E8%A1%8C%E6%AC%A1#%E6%9C%9F%E6%9C%AB%E6%95%B0#%E5%B9%B4%E5%88%9D%E6%95%B0',
                    'showParams': '%5Bobject%20Object%5D',
                    'marginLeft': 0,
                    'marginTop': 0,
                    'eachPageVou': 2,
                    'pagePrint': 1,
                    'js_disPrintMaker': 0,
                    'js_printAttachments': 0,
                    'js_printCover': 0,
                    'isSummary': 0,
                    'level': '', 'dcSummary': 0,
                    'notShowZero': 0,
                    'showSameItem': 0,
                    'showPrintDate': 0,
                    'showPage': 0,
                    'printDate': '2018-07-15',
                    'showQtyPrice': 0,
                    'showCur': 0,
                    'pageSize': '',
                    'pageDirection': 'x',
                    'pageRotationNumber': '',
                    'pageZWY': 0,
                    'fontSize': 9}
            if i < 10:  # 月份数字调整
                a = '%%E8%%B5%%84%%E4%%BA%%A7%%E8%%B4%%9F%%E5%%80%%BA%%E8%%A1%%A8#%s0%s' % (year, i)
                q = "%s0%s" % (year, i)
            else:
                a = '%%E8%%B5%%84%%E4%%BA%%A7%%E8%%B4%%9F%%E5%%80%%BA%%E8%%A1%%A8#%s%s' % (year, i)
                q = "%s%s" % (year, i)
            data['period'] = q
            data['sheetName'] = a

            loginPage = request.post(url, data=data, headers=header, cookies=cookies)  # 获取页面

            file = "D:\\pachong\\账无忧、易代账\\账无忧\\本次资产负债表\\资产负债表" + str(i) + "月.pdf"
            fp = open(file, "w+b")  # 打开一个文本文件
            fp.write(loginPage.content)  # 写入数据i
            fp.close()  # 关闭文件.#抓取资产负债表（1-12月）

            # ——————建立pdfreader，先读出来，放在pdfreader里，方便后续操作。。
            readFile = file

            pdfreader = PyPDF2.PdfFileReader(readFile)

            page1 = pdfreader.getPage(0)
            # ——————建立pdfwriter，先写进到writer里（可以add多页），再导入目标文件。

            # ——————add多个页面到writer

            pdfwriter.addPage(page1)

        # print('抓取资产负债表成功！')
        return pdfwriter

    pdfwriter = tableBalance1()

    # ————利润表
    def tableProfit():  # 抓取利润表(1-12月)
        url = 'http://vip2.kdzwy.com:81/report/report?m=printProfit&reporttype=profit'
        for i in range(mon1, mon2 + 1):
            data = {'dataField': 'name#rownum#balance#prebalance',
                    'columnTitle': '%E9%A1%B9%E7%9B%AE#%E8%A1%8C%E6%AC%A1#%E6%9C%AC%E6%9C%9F%E6%95%B0#%E6%9C%AC%E5%B9%B4%E7%B4%AF%E8%AE%A1%E6%95%B0',
                    # 'sheetName':'%E5%88%A9%E6%B6%A6%E8%A1%A8#2017%E5%B9%B41%E6%9C%9F',#表名时间
                    # 'period':'201701',#表的数据期间
                    'type': 1,
                    'periodParm': 1,
                    'showParams': '%5Bobject%20Object%5D',
                    'marginLeft': 0,
                    'marginTop': 0,
                    'eachPageVou': 2,
                    'pagePrint': 1,
                    'js_disPrintMaker': 0,
                    'js_printAttachments': 0,
                    'js_printCover': 0,
                    'isSummary': 0,
                    'level': 1,
                    'dcSummary': 0,
                    'notShowZero': 0,
                    'showSameItem': 0,
                    'showPrintDate': 0,
                    'showPage': 0,
                    'printDate': '2018-07-17',
                    'showQtyPrice': 0,
                    'showCur': 0,
                    'pageSize': '',
                    'pageDirection': 'x',
                    'pageRotationNumber': '',
                    'pageZWY': 0,
                    'fontSize': 9}

            if i < 10:  # 月份数字调整
                a = '%%E5%%88%%A9%%E6%%B6%%A6%%E8%%A1%%A8#%s%%E5%%B9%%B4%s%%E6%%9C%%9F' % (year, i)  # %s%%E5 year的位置
                q = "%s0%s" % (year, i)
            else:
                a = '%%E5%%88%%A9%%E6%%B6%%A6%%E8%%A1%%A8#%s%%E5%%B9%%B4%s%%E6%%9C%%9F' % (year, i)  # %s%%E5 year的位置
                q = "%s%s" % (year, i)
            data['period'] = q
            data['sheetName'] = a

            loginPage = request.post(url, data=data, headers=header, cookies=cookies)  # 获取页面
            file = "D:/pachong/账无忧、易代账/账无忧/本次利润表/" + str(i) + "月.pdf"
            fp = open(file, "w+b")  # 打开一个文本文件
            fp.write(loginPage.content)  # 写入数据i
            fp.close()  # 关闭文件.#抓取利润表表（1-12月）

            # ——————建立pdfreader，先读出来，放在pdfreader里，方便后续操作。。
            readFile = file
            pdfreader = PyPDF2.PdfFileReader(readFile)
            page1 = pdfreader.getPage(0)

            # ——————add多个页面到writer
            pdfwriter.addPage(page1)
        # ——————writer导入目标文件
        outFile = mkpath
        p = open(outFile + "\\资产负债表和利润表.pdf", "w+b")  # 打开一个文本文件
        p.close()  # 关闭文件.#抓取利润表表（1-12月）

        pdfwriter.write(open(outFile + "\\资产负债表和利润表.pdf", 'wb'))

        # print('抓取利润表成功！')

    # ————凭证
    def pageExport():  # 抓取凭证，默认(1-12)月
        url = 'http://vip2.kdzwy.com:81/gl/voucher?m=printExport&random=1531641125083'
        headers1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Content-Length': '1183',
                    'DNT': '1',
                    'Host': 'vip2.kdzwy.com:81',
                    'Origin': 'http://vip2.kdzwy.com:81',
                    'Proxy-Connection': 'keep-alive',
                    'Referer': 'http://vip2.kdzwy.com:81/print/print-settings-voucher.jsp?type=1&id=1',
                    'Upgrade-Insecure-Requests': '1',
                    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        # coookie='zwyClient=057c3037-44e6-4bf4-8fdd-666305fd30d4; gj-phone=13680010837; Hm_lvt_5bea7f83059ee933473b718b0d0a9f64=1531620760,1531620827,1531620937; Hm_lpvt_5bea7f83059ee933473b718b0d0a9f64=1531620937; _gscu_1096937144=316207608d6k6h11; _gscbrs_1096937144=1; Qs_lvt_151442=1531620760%2C1531620826%2C1531620937; Qs_pv_151442=98633539507137180%2C1304816617309911000%2C1649534967966292200%2C1292840904169476000%2C1182030750131759900; JSESSIONID=7ABE80F3E3F240D6EFAB493827649FFE; ASP.NET_SessionId=mh1sgq0uppyqxhrk2pbfrkio; tencentSig=7350895616; fct=1523522038c1c9afa5a48a6aaaeaf951; fc-phone=13680010837; Hm_lvt_794b82ea3952be1eb6ae7e29afa0d21c=1531620956,1531621409,1531621517,1531639470; Hm_lpvt_794b82ea3952be1eb6ae7e29afa0d21c=1531639470; Hm_lvt_582fb6e62a4f0607ad9f32dafa4efebe=1531620956,1531621409,1531621517,1531639470; Hm_lpvt_582fb6e62a4f0607ad9f32dafa4efebe=1531639470; currentli=0; currentpage=PersonalIndex.aspx; _qddamta_800808582=3-0; thisDbid=7913927920294; Hm_lvt_aa4f230f6878e8cb77ea9eb20c0ff9f3=1531620987; Hm_lpvt_aa4f230f6878e8cb77ea9eb20c0ff9f3=1531653885; _qddaz=QD.jp42cd.ajoigr.jjm7ghw9; _qdda=3-1.319qwv; _qddab=3-94m2xs.jjmqwqty'
        # cookies1 = {i.split('=')[0]: i.split('=')[1] for i in cookie.split(';')}  # ——切片

        data = {'dataField': 'date#mark#summary#subject#debit#credit#people#auditor',
                'fromPeriod': str(year) + str(mon1),  # ————凭证起始时间
                'toPeriod': str(year) + str(mon2),  # ————凭证终止时间
                'columnTitle': '%E6%97%A5%E6%9C%9F#%E5%87%AD%E8%AF%81%E5%AD%97%E5%8F%B7#%E6%91%98%E8%A6%81#%E7%A7%91%E7%9B%AE#%E5%80%9F%E6%96%B9%E9%87%91%E9%A2%9D#%E8%B4%B7%E6%96%B9%E9%87%91%E9%A2%9D#%E5%88%B6%E5%8D%95%E4%BA%BA#%E5%AE%A1%E6%A0%B8%E4%BA%BA',
                'sheetName': '%E5%87%AD%E8%AF%81%E5%88%97%E8%A1%A8#2017%E5%B9%B4%E7%AC%AC1%E6%9C%9F%20%E8%87%B3%202017%E5%B9%B4%E7%AC%AC12%E6%9C%9F',
                # E7%AC%AC+1+%E6——起，E7%AC%AC+12+%E6——终
                'sidx': 'date',
                'sord': 'asc',
                'op': 2,
                'showParams': '%5Bobject%20Object%5D',
                'voucherIds': '',
                ##'199712068034880,200076721419410,200097322777065,200147129401149,200154483500030,200174206800948,200206004496570,200215390309305,200233055802774,200261487620859,200278940908548,200328334582640,200376698059998,200383358743007,200401901587005,200451514128060,200459950668006,200512422345304,206975708166073,206983058558029,206998396810706,207190611051019,207200130305131,207372927760716,207410600055783,207419786800695,207429597072262,207454147059909,406693820528005,414833386262740,415247327093692,415368200957890,416690321575014,416725029750768,416843087765890,418274694667701,418356520192203,418358381700116',
                'marginLeft': 0,
                'marginTop': 0,
                'eachPageVou': 2,
                'pagePrint': 1,
                'js_disPrintMaker': 0,
                'js_printAttachments': 0,
                'js_printCover': 0,
                'isSummary': 0,
                'level': 1,
                'dcSummary': 0,
                'notShowZero': 0,
                'showSameItem': 0,
                'showPrintDate': 0,
                'showPage': 0,
                'printDate': '2018 - 07 - 19',
                'showQtyPrice': 0,
                'showCur': 0,
                'pageSize': 'b5',
                'pageDirection': 'x',
                'pageRotationNumber': '-90',
                'pageScaleWidth': ' 0.7955',
                'pageScaleHeigth': '0.9600',
                'pageZwyWidth': '140',
                'pageZwyHeigth': '240',
                'pageRotationNumberZwy': '-90',
                'pageImgScaleWidth': '0.80',
                'pageImgScaleHeigth': ' 0.96',
                'pageDirectionZwy': 'x',
                'pageZWY': 1,
                'fontSize': 11
                }
        # a = '%%E5%%87%%AD%%E8%%AF%%81%%E5%%88%%97%%E8%%A1%%A8#2017%%E5%%B9%%B4%%E7%%AC%%AC1%%E6%%9C%%9F%%20%%E8%%87%%B3%%202017%%E5%%B9%%B4%%E7%%AC%%AC12%%E6%%9C%%9F'#%%AC%%AC1起%%E6 AC%%AC12终%%
        # data['sheetName'] = a

        loginPage = request.post(url, data=data, headers=headers1, cookies=cookies)  # 获取页面

        zp = open(mkpath + "\\凭证.pdf", "w+b")  # 打开一个文本文件
        zp.write(loginPage.content)  # 写入数据i
        zp.close()  # 关闭文件.#抓取凭证（1-12月）
        # print('抓取凭证成功！')

    # ————明细账
    def exportDetail():  # 抓取明细账，默认1-12月
        url = 'http://vip2.kdzwy.com:81/gl/general?m=printExportDetail'
        data = {'dataField': 'ymd#voucherNo#remark#debit#credit#dcType#balance',
                'columnTitle': '%E6%97%A5%E6%9C%9F#%E5%87%AD%E8%AF%81%E5%AD%97%E5%8F%B7#%E6%91%98%E8%A6%81#%E5%80%9F%E6%96%B9#%E8%B4%B7%E6%96%B9#%E6%96%B9%E5%90%91#%E4%BD%99%E9%A2%9D',
                'sheetName': '%E6%98%8E%E7%BB%86%E8%B4%A6#' + str(year) + '%E5%B9%B4%E7%AC%AC' + str(
                    mon1) + '%E6%9C%9F%20%E8%87%B3%20' + str(year) + '%E5%B9%B4%E7%AC%AC' + str(mon2) + '%E6%9C%9F',
                'op': 2,
                'taodaUrl': '/gl/general?m=notePrintDetail',
                'billType': 'GeneralDetail',
                'fromPeriod': str(year) + str(mon1),  # ——————起明细账时间
                'toPeriod': str(year) + str(mon2),  # ——————终明细账时间

                'accountNum': 1001,
                'number': 1001,
                'accountId': 566904462545066,
                'includeItem': 1,
                'currency': 'RMB',
                'showOppositeAcct': 0,
                'marginLeft': 0,
                'marginTop': 0,
                'eachPageVou': 2,
                'pagePrint': 1,
                'js_disPrintMaker': 0,
                'js_printAttachments': 0,
                'js_printCover': 0,
                'isSummary': 0,
                'level': 1,
                'dcSummary': 0,
                'notShowZero': 0,
                'showSameItem': 0,
                'showPrintDate': 0,
                'showPage': 0,
                'printDate': '2018-07-16',
                'showQtyPrice': 0,
                'showCur': 0,
                'pageSize': '',
                'pageDirection': 'y',
                'pageRotationNumber': '',
                'pageZWY': 0,
                'fontSize': 9}
        loginPage = request.post(url, data=data, headers=header, cookies=cookies)  # 获取页面

        zp = open(mkpath + "\\明细账.pdf", "w+b")  # 打开一个文本文件
        zp.write(loginPage.content)  # 写入数据i
        zp.close()
        # ————数明细账
        readFile = mkpath + "\\明细账.pdf"
        pdfreader = PyPDF2.PdfFileReader(readFile)
        nums = pdfreader.getNumPages()
        RGmx='抓取明细账成功！共%s页' % nums
        os.rename(mkpath + "\\明细账.pdf", mkpath + "\\明细账 %s页.pdf" % nums)
        return RGmx
    # ————总账
    def exportTotal():  # 抓取总账默认1-12月
        url = 'http://vip2.kdzwy.com:81/gl/general?m=printExport&random=1531657739118'
        data = {'dataField': 'yearPeriod#exp#gdebit#gcredit#dcType#gbalance',
                'columnTitle': '%E6%9C%9F%E9%97%B4#%E6%91%98%E8%A6%81#%E5%80%9F%E6%96%B9#%E8%B4%B7%E6%96%B9#%E6%96%B9%E5%90%91#%E4%BD%99%E9%A2%9D',
                'dataField_page': 'number#name#yearPeriod#exp#gdebit#gcredit#dcType#gbalance',
                'columnTitle_page': '%E7%A7%91%E7%9B%AE%E7%BC%96%E7%A0%81#%E7%A7%91%E7%9B%AE%E5%90%8D%E7%A7%B0#%E6%9C%9F%E9%97%B4#%E6%91%98%E8%A6%81#%E5%80%9F%E6%96%B9#%E8%B4%B7%E6%96%B9#%E6%96%B9%E5%90%91#%E4%BD%99%E9%A2%9D',
                'sheetName': '%E6%80%BB%E8%B4%A6#' + str(year) + '%E5%B9%B4%E7%AC%AC' + str(
                    mon1) + '%E6%9C%9F%20%E8%87%B3%20' + str(year) + '%E5%B9%B4%E7%AC%AC' + str(mon2) + '%E6%9C%9F',
                'op': 1,
                'taodaUrl': '/gl/general?m=notePrintGeneral',
                'billType': 'General',
                'fromPeriod': str(year) + str(mon1),  # ————总账时间起始
                'toPeriod': str(year) + str(mon2),  # ————总账时间终止
                'reportitem': '',
                'fromAccountId': '',
                'toAccountId': '',
                'fromLevel': 1,
                'toLevel': 1,
                'includeItem': 0,
                'currency': 'RMB',
                'showParams': '%5Bobject%20Object%5D',
                'marginLeft': 0,
                'marginTop': 0,
                'eachPageVou': 2,
                'pagePrint': 1,
                'js_disPrintMaker': 0,
                'js_printAttachments': 0,
                'js_printCover': 0,
                'isSummary': 0,
                'level': 1,
                'dcSummary': 0,
                'notShowZero': 0,
                'showSameItem': 0,
                'showPrintDate': 0,
                'showPage': 0,
                'printDate': '2018-07-15',
                'showQtyPrice': 0,
                'showCur': 0,
                'pageSize:'','
                'pageDirection': 'x',
                'pageRotationNumber': '',
                'pageZWY': 0,
                'fontSize': 9}
        loginPage = request.post(url, data=data, headers=header, cookies=cookies)  # 获取页面

        zp = open(mkpath + "\\总账.pdf", "w+b")  # 打开一个文本文件
        zp.write(loginPage.content)  # 写入数据i
        zp.close()
        # ————————数总账
        readFile = mkpath + "\\总账.pdf"
        pdfreader = PyPDF2.PdfFileReader(readFile)
        nums = pdfreader.getNumPages()
        os.rename(mkpath + "\\总账.pdf", mkpath + "\\总 %s页.pdf" % nums)
        RGzz='抓取总账成功共%s页！' % nums
        return RGzz

    tableProfit()

    pageExport()

    RGmx=exportDetail()

    RGzz=exportTotal()
    time_end = time.time()
    tkinter.messagebox.showinfo("获取结果", "获取报表成功！        获取凭证成功!                                                   "+RGmx+"         "+RGzz)
Button(root,text='开始',command=start, width=30, height=2).grid(row=5,column=0,columnspan=2,padx=30,pady=5)
Button(root,text='退出',width=30, height=2,command=root.quit).grid(row=6,column=0,columnspan=2,padx=10,pady=5)
photo = PhotoImage(file="D:/pachong/tupiao.png")#file：t图片路径
imgLabel = Label(root,image=photo)
imgLabel.grid(row=9,column=0,rowspan=2,columnspan=2,padx=1,pady=1)

mainloop()



