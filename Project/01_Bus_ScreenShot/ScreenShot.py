import sys
import csv
import pandas as pd
import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=3840x2160')
#options.add_argument('disable-gpu')
try:
    driver = webdriver.Chrome('chromedriver_win32\chromedriver.exe', chrome_options=options)
except:
    driver = webdriver.Chrome(
        '/home/ainochi/Desktop/project/HowToFuzzy/Project/04_BusStop_Infomation/chromedriver_linux64/chromedriver',
        chrome_options=options)

url = "http://121.174.75.24/bims_web/popup2/RealTimeBus.aspx?BNUM="

#output = 'bus/information_predict_arrive_busStop_by'
bus_num_arr = ["17","40","68","81","138-1"]
header = ["Bus_No","Bus_Location","Date"]
time.sleep(3)
csv_file = []
#ps = 0 #테스트 변수
while True:
    now = datetime.datetime.now()
    try:
        # 00시에는 csv파일을 생성한다.
        #if ps == 0:
        if (now.hour == 4) or (now.hour == 16):
            date = now.strftime('%Y%m%d')
            csv_file = []
            for bus_num in bus_num_arr:
                if now.hour > 15 :
                    output_file = 'bus' + bus_num+"/Bus_Location_by"+ bus_num + "_" + str(date) + "_PM.csv"
                else :
                    output_file = 'bus' + bus_num + "/Bus_Location_by" + bus_num + "_" + str(date) + "_AM.csv"
                header_list = [header]
                df = pd.DataFrame(header_list)
                df.to_csv(output_file, index=False, encoding='euc-kr')
                csv_file.append(output_file)
                print("{} 파일이 생성되었습니다.".format(output_file))
            #ps = 1

        # csv_file 배열 안에서 사용할 배열을 초기화
        csv_num = 0
        if (now.hour > 6 and now.hour < 15) or (23 > now.hour and now.hour > 16 ) :
        #if True:
            for bus_num in bus_num_arr:
                url_input = url + bus_num
                driver.get(url_input)
                now = datetime.datetime.now()
                time.sleep(3)

                #확인을 위한 스크린샷
                formatted = now.strftime('%Y%m%d%H%M%S')
                driver.get_screenshot_as_file("Bus" + bus_num + "/" + formatted + "_BusNo" + bus_num + ".png")

                #페이지 파싱
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                bus_location_arr = []
                date = now.strftime('%Y/%m/%d_%H:%M:%S')

                #print(div_conts)
                div_conts = soup.find("div", {"id": "conts"})
                dl = soup.find_all("dl")

                print("위치 정보 뽑기 시작")

                for i in range(0,len(dl)):
                    test = dl[i]
                    test = test.prettify()
                    soup2 = BeautifulSoup(test, 'html.parser')
                    is_bus = soup2.find("p",{"class": "layer_busover2"})
                    if is_bus != None:
                        busStop = str(soup2.find("dd").string).strip()
                        count = i
                        while busStop == "":
                            count -= 1
                            test = dl[count]
                            test = test.prettify()
                            soup2 = BeautifulSoup(test, 'html.parser')
                            busStop = str(soup2.find("dd").string).strip()
                        print("busStop : ", busStop)
                        print("Date : ",date)
                        print(" -----------")

                        bus_loc_info = [bus_num, busStop, str(date)]
                        print(bus_loc_info)
                        column_index = []

                        #date = now.strftime('%Y%m%d')
                        output_file = csv_file[csv_num]
                        print(output_file)

                        # csv파일에 얻은 정보를 추가.
                        with open(output_file, 'a') as csv_out_file:
                            filewriter = csv.writer(csv_out_file)
                            row_index = []
                            for index_value in range(len(header)):
                                column_index.append(index_value)
                                print(bus_loc_info[index_value])
                                row_index.append(bus_loc_info[index_value])
                            filewriter.writerow(row_index)
                csv_num += 1
                print("bus_num = {}".format(bus_num))

        else:
            print("30분 뒤에 다시 실행")
            time.sleep(1800)
    except Exception as e :
        print("오류발생 : ")
        print(e)


#driver.quit()


