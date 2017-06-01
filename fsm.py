from transitions.extensions import GraphMachine

import urllib.request
import re

def get_inf():
    MM = (1 << 31)
    return MM

def cleanhtml(raw_html):
    cleantext = re.sub(r'<.*?>', '', raw_html)
    return cleantext

def clean_whitespace(raw_text):
    cleantext = re.sub(r'\s','', raw_text)
    return cleantext

def clean_letter(raw_text):
    cleantext = re.sub(r'[a-zA-Z]','', raw_text)
    return cleantext

global basicURL
basicURL = 'http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no='

class course:
    def __init__(self):
        self.dept_name = ''         #系所名稱
        self.dept_no = ''           #系所編號
        self.course_num = ''        #課程編號
        self.course_code = ''       #課程編碼
        self.course_name = ''       #課程名稱
        self.course_date = ''       #課程日期
        self.teacher = ''           #指導老師
        self.grade = 0              #年級
        self.grade_detail = ''      #修課班別
        self.credit = 0             #學分
        self.c_e = ''               #必選修
        self.place = ''             #上課地點
        self.cl = 0                 #班別
        self.english = 0            #英語授課
        self.seat = 0               #修課人數上限
        self.cur_seat = 0           #目前修課人數
        self.balance = 0            #餘額
        self.detail = ''            #備註
        self.limit = ''             #限制
        self.moocs = 0              #磨課師

class CourseList:
    def __init__(self, dept_no):
        self.dept_no = dept_no      #系所編號
        self.dept_name = ''         #系所名稱
        self.List = []

########  global data list  ########

course_data = None
DEPT_NO = None
choose = None
search_dept = None
has_get_dept = None
choose2 = None
calen = []
time_table = []

########  global data list  ########

### data function

def data_build():
    global course_data
    global DEPT_NO
    global calen
    global time_table
    DEPT_NO = ['A2','A3','A4','A5','A6','AA','AH', \
               'AN','C0', \
               'A1','A7','A9','AG', \
               'B0','B1','B2','B3','B5','K1','K2','K3','K4','K5','K7','K8', \
               'C1','C2','C3','C4','CZ','F8', \
               'L1','L2','L3','L4','L7','LA','VF', \
               'E0','E1','E3','E4','E5','E6','E8','E9','F0','F1','F4','F5','F6','F9', \
               'N1','N3','N4','N5','N6','N8','NC','N9','P0','P1','P4','P5','P6','P8','Q4','N0','NA','NB', \
               'H1','H2','H3','H4','H5','R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','RA','RB','RD','RZ', \
               'I2','I3','I5','I6','I7','I8','T1','T2','T3','T4','T6','T7','T8','T9','TA','TC',\
               'S0','S1','S2','S3','S4','S5','S6','S7','S8','S9','SA','SB','SC',\
               'D2','D4','D5','D8','U1','U2','U3','U5','U7',\
               'E2','F7','N2','ND','P7','P9','Q1','Q3','Q5','Q6','Q7',\
               'V6','V8','V9','VA','VB','VC','VD','VE','VG','VH','VJ','VK','VL','VM','VN',\
               'E7','F2','F3','N7','P2','P3','PA','PB',\
               'C5','C6','L5','L6','Z0','Z2','Z3','Z5'
              ]
    course_data = []
    calen = []
    time_table = ['0','1','2','3','4','N','5','6','7','8','9','A','B','C','D','E']
    for i in range(7):
        new = []
        for j in range(16):
            new.append('NON')
        calen.append(new)
        print("get: " + str(calen[i][0]))
    for dept in DEPT_NO:################ DEBUG #################
        temp_dept = CourseList(dept)

        req = urllib.request.Request(basicURL + temp_dept.dept_no)
        print("get url start\n")
        content = urllib.request.urlopen(req, timeout=120).read()

        url = re.split(b"<TR class='course_y[0-9]'>", content)
        pre_course = ''
        for i in range(len(url)):
            if ( i == 0 ):
                continue
            else:
                temp_course = course()
                course_info = re.split(b"</TD>", url[i])
                for j in range(len(course_info)):
                    info = cleanhtml(course_info[j].decode('utf-8'))
                    clean_info = clean_whitespace(info)
                    if ( clean_info == '' ):
                        continue
                    if (j == 0):
                        clean_dept = clean_letter(clean_info)
                        temp_dept.dept_name = clean_dept
                        temp_course.dept_name = clean_dept
                    elif (j == 1):
                        temp_course.dept_no = dept
                    elif (j == 2):
                        temp_course.course_num = clean_info
                        #if ( clean_info != '' ):
                        #    print("course num : " + clean_info + "\n")
                    elif (j == 3):
                        temp_course.course_code = clean_info
                    elif (j == 4):
                        pass
                    elif (j == 5):
                        temp_course.grade_detail = clean_info
                    elif (j == 6):
                        temp_course.grade = int(clean_info)
                    elif (j == 7):
                        pass
                    elif (j == 8):
                        pass
                    elif (j == 9):
                        if ( clean_info.find("Y") != -1 ):
                            temp_course.english = 1
                        else:
                            temp_course.english = 0
                    elif (j == 10):
                        temp_course.course_name = clean_info
                    elif (j == 11):
                        temp_course.c_e = clean_info
                    elif (j == 12):
                        temp_course.credit = int(clean_info)
                    elif (j == 13):
                        temp_course.teacher = clean_info
                    elif (j == 14):
                        temp_course.cur_seat = int(clean_info)
                    elif (j == 15):
                        if ( clean_info.find('額滿') != -1 ):
                            temp_course.balance = 0
                        elif ( clean_info.find('不限') != -1 ):
                            temp_course.balance = get_inf()
                        else:
                            temp_course.balance = int(clean_info)
                    elif (j == 16):
                        temp_course.course_date = clean_info
                    elif (j == 17):
                        temp_course.place = clean_info
                    elif (j == 18):
                        temp_course.detail = clean_info
                    elif (j == 19):
                        temp_course.limit = clean_info
                    elif (j == 23):
                        if ( clean_info.find("是") != -1 ):
                            temp_course.moocs = 1 
                        else:
                            temp_course.moocs = 0
                    else:
                        pass
                if ( temp_course.course_num != '' ):
                    #print("add course: " + temp_course.course_name + "\n")
                    temp_dept.List.append(temp_course)
                    pre_course = temp_course.course_name
                elif ( temp_course.course_name == pre_course ):
                    #print("Same course\n")
                    if ( temp_dept.List[len(temp_dept.List) - 1].course_date.find(temp_course.course_date) == -1 ):
                        temp_dept.List[len(temp_dept.List) - 1].course_date += temp_course.course_date 
                        #print("course date: " + temp_dept.List[len(temp_dept.List) - 1].course_date + "\n")
        course_data.append(temp_dept)
        print("dept name: " + temp_dept.dept_name + " OK!\n")

def check_lcs(word1, word2):
    j = 0
    if ( word1.find(word2) != -1 ):
        return 1
    elif ( word1.find(word2.upper()) != -1 ):
        return 1
    for i in range(len(word1)):
        if ( word1[i] == word2[j] ):
            j += 1
        if ( j == len(word2) ):
            return 1
    return 0

def search_data(search_word):
    global DEPT_NO
    global course_data
    global choose
    global search_dept
    global choose2
    find_set = []
    if choose == 1:
        for i in range(len(DEPT_NO)):
            for j in range(len(course_data[i].List)):
                if course_data[i].List[j].course_num == search_word:
                    find_set.append(course_data[i].List[j])
    elif choose == 2:
        for i in range(len(DEPT_NO)):
            for j in range(len(course_data[i].List)):
                check = check_lcs(course_data[i].List[j].course_name, search_word)
                if check == 1:
                    find_set.append(course_data[i].List[j])
    elif choose == 3:
        if has_get_dept == 0:
            for i in range(len(DEPT_NO)):
                if course_data[i].dept_name == search_word:
                    find_set.append(search_word)
        else:
            find_set = []
            '''
            if choose2 == 1:
                for i in range(len(search_dept))
            elif choose2 == 2:

            elif choose3 == 3:
            '''
    return find_set

### initial message

def init_message():
    text =  "歡迎使用泥鴿成大課程資訊查詢系統\n\n" + \
            "輸入\"查詢\"使用查詢功能\n" + \
            "輸入\"課表安排\"來安排課表\n" + \
            "輸入\"更多功能\"查看其他功能\n" + \
            "若重新登入請輸入任意文字來重新使用"
    return text

### Machine transition define

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
        #update.message.reply_text("Initialize succeed")

    def bot_init(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no input'
        if text == '/start':
            reply_word = init_message()
            update.message.reply_text(reply_word)
            return 1
        else:
            return 0

    def is_going_to_search(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no input'
        return text.lower() == '查詢'

    def is_going_to_calendar(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no input'
        return text.lower() == '課表安排'

    def is_going_to_search_mid(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no'
        c = re.sub(r'[A-Za-z]','', text)
        global choose
        if len(c) == 1 and c.isdigit() :
            choose = int(text)
            if choose == 1 or choose == 2 or choose == 3:
                return 1
            else:
                reply_t = "123而已很難打???\n"
                update.message.reply_text(reply_t)
                return 0
        else:
            reply_t = "123而已很難打???\n"
            update.message.reply_text(reply_t)
            return 0

    def is_going_to_search_end(self, update):
        global choose
        global has_get_dept
        global search_dept
        global choose2
        reply_word = ''
        pre_dept = ''
        if update.message != None:
            text = update.message.text
        else:
            text = 'no'
        if text == 'no':
            return 0
        if ( choose == 1 ):
            search_word = re.sub(r'[A-Za-z\n]','',text)
            if ( len(search_word) == 3 and search_word.isdigit() ):
                result = search_data(search_word)
                if ( len(result) == 0 ):
                    reply_word = "沒有符合的結果\n你南大生???\n"
                else:
                    reply_word = reply_word + "查詢結果如下:\n\n"
                    for res in result:
                        if pre_dept != res.dept_name:
                            reply_word = reply_word + res.dept_name + ":\n"
                            pre_dept = res.dept_name
                        reply_word = reply_word + "    系所編號：\t" + res.dept_no + "\n"
                        reply_word = reply_word + "    課程編號：\t" + res.course_num + "\n"
                        reply_word = reply_word + "    課程名稱：\t" + res.course_name + "\n"
                        reply_word = reply_word + "    指導老師：\t" + res.teacher + "\n"
                        reply_word = reply_word + "    修課人數：\t" + str(res.cur_seat) + "\n"
                        reply_word = reply_word + "    修課時間：\t" + res.course_date + "\n"
                        reply_word = reply_word + "    修課地點：\t" + res.place + "\n"
                        reply_word = reply_word + "    學分數目：\t" + str(res.credit) + "\n\n"
                update.message.reply_text(reply_word)
                return 1
            else:
                reply_word = "3個數字而已\n你腦中風???\n"
                update.message.reply_text(reply_word)
                return 0
        elif ( choose == 2 ):
            search_word = text#re.sub(r'[A-Za-z]','',text)
            if search_word != '':
                result = search_data(search_word)
                if ( len(result) == 0 ):
                    reply_word = "沒有符合的結果\n你南大生???\n"
                else:
                    reply_word = reply_word + "查詢結果如下:\n\n"
                    for res in result:
                        if pre_dept != res.dept_name:
                            reply_word = reply_word + res.dept_name + ":\n"
                            pre_dept = res.dept_name
                        reply_word = reply_word + "    系所編號：\t" + res.dept_no + "\n"
                        reply_word = reply_word + "    課程編號：\t" + res.course_num + "\n"
                        reply_word = reply_word + "    課程名稱：\t" + res.course_name + "\n"
                        reply_word = reply_word + "    指導老師：\t" + res.teacher + "\n"
                        reply_word = reply_word + "    修課人數：\t" + str(res.cur_seat) + "\n"
                        reply_word = reply_word + "    修課時間：\t" + res.course_date + "\n"
                        reply_word = reply_word + "    修課地點：\t" + res.place + "\n"
                        reply_word = reply_word + "    學分數目：\t" + str(res.credit) + "\n\n"
                update.message.reply_text(reply_word)
                return 1
            else:
                update.message.reply_text("請講中文")
                return 0
        elif ( choose == 3 ):
            print("\"" + text + "\"")
            reply_word = ''
            che = 0
            for dept in course_data:
                print("\"" + dept.dept_name + "\"")
                i = 0
                for j in range(len(dept.dept_name)):
                    if ( text[i] == dept.dept_name[j] ):
                        i += 1
                    if ( i == len(text) ):
                        che = 1
                        break
                if ( che == 1 ):
                    reply_word = reply_word + "查詢結果如下:\n\n"    
                    for res in dept.List:
                        reply_word = reply_word + "    系所編號：\t" + res.dept_no + "\n"
                        reply_word = reply_word + "    課程編號：\t" + res.course_num + "\n"
                        reply_word = reply_word + "    課程名稱：\t" + res.course_name + "\n"
                        reply_word = reply_word + "    指導老師：\t" + res.teacher + "\n"
                        reply_word = reply_word + "    修課人數：\t" + str(res.cur_seat) + "\n"
                        reply_word = reply_word + "    修課時間：\t" + res.course_date + "\n"
                        reply_word = reply_word + "    修課地點：\t" + res.place + "\n"
                        reply_word = reply_word + "    學分數目：\t" + str(res.credit) + "\n\n"
                    break
            if reply_word != '':
                update.message.reply_text(reply_word)
            else:
                update.message.reply_text("你錯字系？？\n")
            return 1

        '''
            search_word = re.sub(r'[A-Za-z]','',text)
            if has_get_dept == 0:
                if search_word != '':
                    result = search_data(search_word)
                    if ( len(result) == 0 ):
                        reply_word = "沒有符合的結果\n你南大生???\n"
                    else:
                        search_dept = result[0]
                        has_get_dept = 1
                        reply_word = "請問想要以何種資訊查詢課程?\n\n" + \
                            "1.課程名稱" + \
                            "2.課程時間" + \
                            "3.課程年級"
                    update.message.reply_text(reply_word)
                else:
                    update.message.reply_text("請講中文")
                return 0
            elif has_get_dept == 1:
                has_get_dept = 2
                if search_word.isdigit() and len(search_word) == 1:
                    choose2 = int(search_word)
                    if ( choose2 == 1 ):
                        reply_word = "請輸入欲查詢之課程名稱"
                    elif ( choose2 == 2 ):
                        reply_word = "請輸入欲查詢之課程時間"
                    elif ( choose2 == 3 ):    
                        reply_word = "請輸入欲查詢之課程年級"
                    update.message.reply_text(reply_word)
                    return 0
                else:
                    update.message.reply_text("好好選, 好嗎")
                    return 0
            elif has_get_dept == 2:
                has_get_dept = 0
                return 1
        '''
    def is_going_to_black(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no input'
        return text.lower() == '更多功能'

    def is_going_to_black_end(self, update):
        if update.message != None:
            text = update.message.text
        else:
            text = 'no input'
            return 0
        if len(text) == 1 and text.isdigit() :
            choose = int(text)
            if choose == 1 or choose == 2 or choose == 3:
                return 1
            else:
                reply_t = "123而已很難打???\n"
                update.message.reply_text(reply_t)
                return 0
        else:
            reply_t = "123而已很難打???\n"
            update.message.reply_text(reply_t)
            return 0
        

    def is_going_to_calendar_end(self, update):
        global course_data
        global DEPT_NO
        global calen
        global time_table
        text = ''
        if update.message != None:
            text = update.message.text
        else:
            text = 'no'
        if text == 'no':
            return 0
        course_n = re.split(r'\s', text)
        temp_cal = []
        t = None
        if ( len(course_n) == 2 ):
            dept_n = course_n[0]
            cou_n = course_n[1]
            for dep in course_data:
                if dept_n == dep.dept_no:
                    for cou in dep.List:
                        if cou.course_num == cou_n:
                            t = cou
                            break
                if t != None:
                    break
            if ( t != None ):
                get_date = re.findall(r'\[[0-9]\][0-9]~[0-9]|\[[0-9]\][0-9A-EN]', t.course_date)
                print(t.course_date)
                print("get Date : ")
                print(get_date)
                day = 0
                top = 0
                bottom = 0
                for date in get_date:
                    day = int(date[1]) - 1
                    if ( date.find("~") != -1 ):
                        top = time_table.index(date[3])
                        bottom = time_table.index(date[5]) + 1
                        print(str(top) + "    " + str(bottom))
                        for j in range(top, bottom):
                            if ( calen[day][j] != 'NON' ):
                                update.message.reply_text("衝堂啦ㄤ9\n")
                                return 0
                    else:
                        top = time_table.index(date[3])
                        if ( calen[day][top] != 'NON' ):
                            update.message.reply_text("衝堂啦ㄤ9\n")
                            return 0
                for date in get_date:
                    day = int(date[1]) - 1
                    if ( date.find("~") != -1 ):
                        top = time_table.index(date[3])
                        bottom = time_table.index(date[5]) + 1
                        for j in range(top, bottom):
                            calen[day][j] = t.course_name[0]
                    else:
                        bottom = time_table.index(date[3])
                        print(str(bottom))
                        calen[day][bottom] = t.course_name[0]
                        bottom += 1
                update.message.reply_text("加入課程：\n    " + t.course_name)
                return 0
            else:
                update.message.reply_text("無此課程\n87\n")
        else:
            if ( text.upper() == 'OK' ):
                reply_word = "--    一    二    三    四    五\n"
                for i in range(len(time_table)):
                    reply_word = reply_word + time_table[i] + "    "
                    for j in range(5):
                        if ( calen[j][i] != 'NON' ):
                            reply_word = reply_word + calen[j][i] + "    "
                            calen[j][i] = 'NON'
                        else:
                            reply_word = reply_word + "        "
                    reply_word = reply_word + "    \n"
                update.message.reply_text("你的課表如下：\n\n")
                update.message.reply_text(reply_word)
                return 1
            else:
                update.message.reply_text("好好打好ㄇ ^^\n")
                return 0

    def on_enter_search(self, update):
        reply_t = "請問你想以何種資訊查詢課程？\n\n" + \
                "1.課程編碼\n" + \
                "2.課程名稱\n" + \
                "3.所屬系所\n"
        update.message.reply_text(reply_t)
        #text = init_message()
        #update.message.reply_text(text)

    def on_enter_search_mid(self, update):
        global choose
        reply_t = ""
        if ( choose == 1 ):
            reply_t = "請輸入欲查詢之課程編碼\n"
        elif ( choose == 2 ):
            reply_t = "請輸入欲查詢之課程名稱\n" + \
                    "或是課程簡稱 (e.g. 計組, 普物)\n"
        elif ( choose == 3 ):
            reply_t = "請輸入欲查詢之所屬系所中文名稱\n"
        update.message.reply_text(reply_t)

    def on_enter_calendar(self, update):
        update.message.reply_text("請輸入系所及課程編碼\n格式 : {系所編碼} {課程編碼}\n若結束請輸入\"OK\"")

    def on_enter_search_end(self, update):
        text = init_message()
        update.message.reply_text(text)
        self.go_back(update)

    def on_enter_black(self, update):
        reply_word = "你想使用哪些功能\n" + \
                    "1.餘額鬧鐘(可在該課程有餘額時通知)\n" + \
                    "2.搶課幫手(幫助使用者搶課)\n" + \
                    "3.課程評論\n"
        update.message.reply_text(reply_word)

    def on_enter_black_end(self, update):
        text = "你要求很多\n"
        update.message.reply_text(text)
        text = init_message()
        update.message.reply_text(text)
        self.go_back(update)
    
    def on_enter_calendar_end(self, update):
        text = init_message()
        update.message.reply_text(text)
        self.go_back(update)

    def on_exit_search(self, update):
        print('Leaving search\n')

    def on_exit_search_mid(self, update):
        print('Leaving search_mid')

    def on_exit_calendar(self, update):
        print('Leaving calendar\n')

    def on_exit_search_end(self, update):
        print("Leaving search_end\n")

    def on_exit_black(self, update):
        print("Leaving black\n")

    def on_exit_black_end(self, update):
        print("Leaving black end\n")

    def on_exit_calendar_end(self, update):
        print("Leaving calendar_end\n")
