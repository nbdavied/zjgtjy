import httpUtil
import re
import mysql.connector

list_url = "http://land.zjgtjy.cn/GTJY_ZJ/deala_js_action?resourcelb=01&dealtype=&JYLB=&JYFS=&JYZT=&RESOURCENO=&RESOURCEMC=&endDate=&ZYWZ=&zylb=01&currentPage="
detail_url = "http://land.zjgtjy.cn/GTJY_ZJ/landinfo?ResourceID="
time_url = "http://land.zjgtjy.cn/GTJY_ZJ/time?id="

START_PAGE = 1
END_PAGE = 50
DB_CONFIG={}
def getValueFromPage(key, page):
    """
    从页面获取数据
    """
    try:
        value = re.findall(key + "\s*</td>.*?>\s*(.*?)\s*</td>", page, re.S)[0]
        value = value.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        #print(key, value)
    except:
        value = ""
    return value

def getStatus(id):
    """
    查询交易状态
    """
    time_page = httpUtil.http_get(time_url + id, charset="gbk")
    showTimeFunction = re.search("show_date_time", time_page)
    if showTimeFunction:
        status = "0"
    else:
        s = re.findall("<font style='font-size:18px;font-weight:bold;'>(.*?)</font>", time_page)[0]
        s = s.replace(".","")
        if s == "已成交" or s == "交易结束":
            status = "1"
        elif s =="结束" or s == "未成交" or s == "终止" or s =="中止":
            status = "2"
        elif s=="正在竞价" or s == "正在等待期":
            status = "0"
    return status

# 选择查询区域，获得cookie
# nb_url = "http://land.zjgtjy.cn/GTJY_ZJ/runtime_prj?canton=330200"
# response, header_cookie = httpUtil.http_get_cookie(nb_url, charset="gbk")
# cookies = header_cookie.split(",")
# session = ""
# for cookie in cookies:
#     cookie = cookie.strip(" ")
#     if cookie.startswith("JSESSIONID"):
#         session = cookie.split(';')[0]
#         break




CONN = mysql.connector.connect(user=DB_CONFIG['user'],
                               password=DB_CONFIG['password'],
                               host=DB_CONFIG['host'],
                               database=DB_CONFIG['database'])
CURSOR = CONN.cursor()
#查询未结束交易状态
def checkStatus():
	CONN2 = mysql.connector.connect(user=DB_CONFIG['user'],
                               password=DB_CONFIG['password'],
                               host=DB_CONFIG['host'],
                               database=DB_CONFIG['database'])
	update = CONN2.cursor()
	sql = "select id from zjgtjy where status = '0'"
	CURSOR.execute(sql)
	row = CURSOR.fetchone()
	while row:
	    id = str(row[0])
	    status = getStatus(id)
	    if status == "1":
	        detail_page = httpUtil.http_get(detail_url + id, charset="gbk")
	        cjsj = getValueFromPage("成交时间", detail_page)
	        cjj = getValueFromPage("成交价", detail_page)
	        cjj = cjj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
	        #print("成交价", cjj)
	        jddw = getValueFromPage("竞得单位", detail_page)
	        jssj = getValueFromPage("结束时间", detail_page)
	        zgbj = getValueFromPage("最高报价", detail_page)
	        zgbj = zgbj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
	        #print("最高报价", zgbj)
	        zgbjdw = getValueFromPage("最高报价单位", detail_page)
	        cjsj = cjsj + jssj
	        cjj = cjj + zgbj
	        jddw = jddw + zgbjdw
	        sql = "update zjgtjy set cjsj = '%s', cjj = '%s', jddw = '%s', status = '1' where id = %s" % (cjsj, cjj, jddw, id)
	        update.execute(sql)
	        CONN2.commit()
	    elif status == "2":
	        sql = "update zjgtjy set status = '2' where id = %s" % (id)
	        update.execute(sql)
	        CONN2.commit()
	    row = CURSOR.fetchone()
	update.close()
	CONN2.close()
	
checkStatus()
for i in range(START_PAGE, END_PAGE + 1):
    print("\r\n-------------------开始查询第" + str(i) + "页---------------------\r\n")
    #list_page = httpUtil.http_get(list_url + str(i),charset="gbk", cookie=session)
    list_page = httpUtil.http_get(list_url + str(i),charset="gbk")
    ids = re.findall("javascript:goRes\('(\d*)','01'\)", list_page)
    for id in ids:
        if id=="12443" or id=="12783" or id=="13081" or id=="13077" or id=="16175" or id=="16176" or id=="18179" or id=="18180":
            continue
        #id="8382"
        sql = "select * from zjgtjy where id=%s" % id
        CURSOR.execute(sql)
        if CURSOR.fetchall():
            #已经存在数据
            continue
        detail_page = httpUtil.http_get(detail_url + id, charset="gbk")
        print("发现新地块, id", id)
        dkbh = getValueFromPage("地块编号", detail_page)
        print("地块编号", dkbh)
        pm_start_time = getValueFromPage("拍卖开始时间", detail_page)
        jj_start_time = getValueFromPage("限时竞价开始时间", detail_page)
        gp_start_time = getValueFromPage("挂牌起始时间", detail_page)
        gp_stop_time = getValueFromPage("挂牌截止时间", detail_page)
        bm_start_time = getValueFromPage("报名开始时间", detail_page)
        bm_stop_time = getValueFromPage("报名截止时间", detail_page)
        bzj_stop_time = getValueFromPage("保证金到账截止时间", detail_page)
        have_dj = getValueFromPage("是否有底价", detail_page)
        dkmc = getValueFromPage("地块名称", detail_page)
        print("地块名称", dkmc)
        tdwz = getValueFromPage("土地位置", detail_page)

        tdyt = getValueFromPage("土地用途", detail_page)
        tdyt = tdyt.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        #print("土地用途", tdyt)
        rjl = getValueFromPage("容积率", detail_page)
        try:
            rjl = rjl.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
            rjl = re.findall("[<≤]容积率[<≤](.*?)$", rjl)[0]
        except:
            pass
        ssxzq = getValueFromPage("所属行政区", detail_page)
        crmj = getValueFromPage("出让面积", detail_page)
        if crmj == "":
            crmj = getValueFromPage("租赁面积", detail_page)
            if crmj == "":
                continue
        crmj = re.findall("(.*?)\（", crmj)[0]
        crmj = crmj.replace("平方米", "")
        #print("出让面积", crmj)
        crnx = getValueFromPage("出让年限", detail_page)
        qsj = getValueFromPage("起始价", detail_page)
        qsj = qsj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        bzj = getValueFromPage("竞买保证金", detail_page)
        bzj = bzj.replace("万元", "")
        zjfd = getValueFromPage("竞价增价幅度", detail_page) 
        zgxj = getValueFromPage("最高限价", detail_page)
        zgxj = zgxj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        #print("最高限价", zgxj)
        tdwz = getValueFromPage("土地位置", detail_page)
        tbzgzcbl = getValueFromPage("投报最高自持比例", detail_page)
        tbzccsbl = getValueFromPage("投报自持初始比例", detail_page)
        tbzcblfd = getValueFromPage("投报自持比例幅度", detail_page)
        ptyfqsmj = getValueFromPage("配套用房起始面积", detail_page)
        tbptyffd = getValueFromPage("投报配套用房幅度", detail_page)
        tzqd = getValueFromPage("固定资产投资强度", detail_page)
        jmrtj = getValueFromPage("竞买人条件", detail_page)
        try:
            jmrtj = re.findall("<div.+?>\s*(.*?)\s*</div>", jmrtj, re.S)[0]
            jmrtj = jmrtj.replace("\r", "").replace("\n","").replace("'","\\'")
            #print("竞买人条件", jmrtj)
        except:
            pass
        lxr = getValueFromPage("联系人", detail_page)
        lxrdh = getValueFromPage("联系人电话", detail_page)
        lxrdz = getValueFromPage("联系人地址", detail_page)
        cjsj = getValueFromPage("成交时间", detail_page)
        cjj = getValueFromPage("成交价", detail_page)
        cjj = cjj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        #print("成交价", cjj)
        jddw = getValueFromPage("竞得单位", detail_page)
        jssj = getValueFromPage("结束时间", detail_page)
        zgbj = getValueFromPage("最高报价", detail_page)
        zgbj = zgbj.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
        #print("最高报价", zgbj)
        zgbjdw = getValueFromPage("最高报价单位", detail_page)
        #查询状态
        status = getStatus(id)
        if status == "1":
            cjsj = cjsj + jssj
            cjj = cjj + zgbj
            jddw = jddw + zgbjdw
        
        sql = ("insert into zjgtjy ("
                "id, dkbh, gp_start_time, gp_stop_time, pm_start_time,"
                "jj_start_time, bm_start_time, bm_stop_time, bzj_stop_time,"
                "have_dj, dkmc, tdwz, tdyt, rjl, ssxzq, crmj, crnx, qsj, bzj,"
                "zjfd, tzqd, jmrtj, lxr, lxrdh, lxrdz, zgxj, tbzgzcbl,"
                "tbzccsbl, tbzcblfd, ptyfqsmj, tbptyffd, cjsj, cjj, jddw, status) "
                "values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',"
                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',"
                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',"
                "'%s', '%s', '%s', '%s', '%s')") % (id, dkbh, gp_start_time, gp_stop_time, pm_start_time,
                                                                jj_start_time, bm_start_time, bm_stop_time, bzj_stop_time,
                                                                have_dj, dkmc, tdwz, tdyt, rjl, ssxzq, crmj, crnx, qsj, bzj,
                                                                zjfd, tzqd, jmrtj, lxr, lxrdh, lxrdz, zgxj, tbzgzcbl,
                                                                tbzccsbl, tbzcblfd, ptyfqsmj, tbptyffd, cjsj, cjj, jddw, status)
        CURSOR.execute(sql)
        CONN.commit()
        #break



CURSOR.close()
CONN.close()


print("执行完毕")