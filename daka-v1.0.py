# -*- coding: UTF-8 -*- 
import time
import requests
from selenium import webdriver
import json

def longTime():
    data_start = input("请输入起始的日期：")
    data_end = input("请输入结束的日期：")
    student_list = []
    student_list1 = []
    with open("./学生党支部.txt", "r") as myfile:
        student_list = myfile.readlines()

    for i in range(len(student_list)):
        student_list[i]=student_list[i].strip()

    with open("./学生党支部.txt", "r") as myfile:
        student_list1 = myfile.readlines()

    for i in range(len(student_list1)):
        student_list1[i] = student_list1[i].strip()

    teacher_list = []
    teacher_list1 = []
    with open("./教工党支部.txt", "r") as myfile:
        teacher_list = myfile.readlines()

    for i in range(len(teacher_list)):
        teacher_list[i] = teacher_list[i].strip()

    with open("./教工党支部.txt", "r") as myfile:
        teacher_list1 = myfile.readlines()

    for i in range(len(teacher_list1)):
        teacher_list1[i] = teacher_list1[i].strip()

    #print(student_list)
    #return
    member_data=[]
    url = 'https://study.xuexi.cn/admin/index.html#/report/organization'
    chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
    wd = webdriver.Chrome(executable_path=chromePath)
    wd.get(url)
    time.sleep(30)  # 设定30秒睡眠，期间进行手动登陆。十分关键，下面有解释。
    cookies = wd.get_cookies()  # 调出Cookies
    req = requests.Session()
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])
    header = {'Referer': ' https://study.xuexi.cn/'}
    member_url = 'https://smp.xuexi.cn/api/report/org/memberList'

    for i in range(int(data_start),int(data_end)+1):
        time.sleep(0.5)
        member_json = {"startDate": str(i), "endDate": str(i), "pageNo": 1, "pageSize": 200, "sort": "totalScore","asc": "false"}
        member_result = requests.post(url=member_url, headers=header, json=member_json, cookies=req.cookies.get_dict())
        member_data=json.loads(member_result.text)
        print(member_data['data']['list'])

        for list in member_data['data']['list']:
            for i in range(len(student_list1)):
                if list['userName'] == student_list1[i]:
                    if list['rangeScore'] <10 :
                        student_list[i]=student_list[i]+'  不达标'
                    else:
                        student_list[i]=student_list[i]+'  √'
                    break
        print(student_list1)
        print(student_list)
        with open("./result_student.txt", "w+") as myfile:
            for each in student_list:
                myfile.write(each+'\n')

            for list in member_data['data']['list']:
                for i in range(len(teacher_list1)):
                    if list['userName'] == teacher_list1[i]:
                        if list['rangeScore'] < 10:
                            teacher_list[i] = teacher_list[i] + '  不达标'
                        else:
                            teacher_list[i] = teacher_list[i] + '  √'
                        break
            print(teacher_list1)
            print(teacher_list)
            with open("./result_teacher.txt", "w+") as myfile:
                for each in teacher_list:
                    myfile.write(each + '\n')


#全部
def today():
#    data_today=input("请输入今天的日期：")
    data_today = str(int(time.strftime("%Y%m%d", time.localtime()))-1)
    print(data_today)
    print("--------------------")
    url = 'https://study.xuexi.cn/admin/index.html#/report/organization'
    chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver'
    wd = webdriver.Chrome(executable_path=chromePath)
    wd.get(url)
    time.sleep(30)  # 设定30秒睡眠，期间进行手动登陆。十分关键，下面有解释。
    cookies = wd.get_cookies()  # 调出Cookies
    ret =''
    req = requests.Session()
    for cookie in cookies:
        cookie_name=cookie['name']
        cookie_value=cookie['value']
        ret=ret+cookie_name+'='+cookie_value+';' #ret即为最终的cookie，各cookie以“;”相隔开    
    
    header = {
            'Referer': 'https://study.xuexi.cn/',
    		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
			"Accept": "application/json, text/plain, */*",
			"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
			"Content-Type": "application/json;charset=utf-8",
			"Origin": "https://study.xuexi.cn",
			"cookie":ret
    			}
    member_url = 'https://odrp.xuexi.cn/report/commonReport'
    member_json = {"apiCode":"ab4afc14","dataMap":{"startDate":data_today,"endDate":data_today,"offset":0,"sort":"rangeScore","pageSize":200,"order":"asc","isActivate":"","orgGrayId":"doXB1RFMspKyJl94n5RUiQ=="}}
    member_json1=json.dumps(member_json)
    member_result = requests.post(url=member_url,headers=header,data=member_json1)
    print("--------------result------------")
    member_data = json.loads(member_result.text)
    member_data['data_str'] = json.loads(member_data['data_str'])
    print(member_data)
    print("------------------")
    #with open("./Party.txt", "w+") as myfile:
        #for list in member_data['data']['list']:
            #myfile.write(str(list['userName']).ljust(3) + '<------>' + str(list['rangeScore'])+'------'+str(list['deptNames']))
            #myfile.write("\n")
    flag=0
	
    with open("./"+data_today+".txt","w+") as myfile:
        myfile.write(data_today[4:6]+"月"+data_today[6:8]+"日学习情况通报：以下同志未达到10分要求\n")
        myfile.write("学生党支部 : ")
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院学生党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore'])+'.0分)')
                flag+=1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")

        myfile.write("研究生本研党支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院本研学生联合党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")
 
        myfile.write("研究生第一党支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院研究生第一党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")
        
        myfile.write("研究生第二党支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院研究生第二党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")
        
        myfile.write("研究生第三党支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院研究生第三党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")
        

        myfile.write("计算机支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院计算机系教工党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")

        myfile.write("电子支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院电子工程系教工党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
        myfile.write("\n")

        myfile.write("行政支部 : ")
        flag = 0
        for list in member_data['data_str']['dataList']['data']:
            if list['rangeScore'] < 10 and list['deptNames'].find("信息工程学院行政教工党支部")>-1:
                print(list['userName'].ljust(3))
                if flag!=0:
                    myfile.write(",")
                myfile.write(str(list['userName']).ljust(3) + '(' + str(list['rangeScore']) + '.0分)')
                flag += 1
        if flag==0:
            myfile.write('无')
            


#a=input("请问你想要的操作是：1.查询当天未达标成员  2.查询一段时间内的未达标统计表格:")
#if a=='1':
today()
#elif a=='2':
#    longTime()
print("good")
#{'ddId': 580286504, 'userName': '张三', 'deptId': 150004435611, 'deptNames': '信息工程学院学生党支部', 'state': '激活', 'rangeScore': 23.0, 'totalScore': 5544.0}
