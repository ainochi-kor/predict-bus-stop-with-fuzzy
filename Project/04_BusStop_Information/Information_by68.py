import pandas as pd
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime

#드라이버를 실행한다.
options = webdriver.ChromeOptions()
options.add_argument('headless')

try:
    driver = webdriver.Chrome('chromedriver_win32\chromedriver.exe',chrome_options=options)
except :
    driver = webdriver.Chrome('/home/ainochi/Desktop/project/HowToFuzzy/Project/04_BusStop_Infomation/chromedriver_linux64/chromedriver',chrome_options=options)
url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%B6%80%EC%82%B0+10134&oquery=%EB%B6%80%EC%82%B0+%EC%A0%95%EB%A5%98%EC%9E%A5&tqi=UW5oxlp0J1ssscae77sssssssQV-445300"
driver.get(url)

input_file = 'refine/busStop_Refine_by68.csv'
output = 'Information/information_predict_arrive_busStop_by68'

header = ['BusStop_No', 'BusStop_Name', 'Bus_No', 'Predict_Arrive', 'Current_Time']
data_frame = pd.read_csv(input_file, encoding='euc-kr')

arr_num = []
for num in range(12,81):
    arr_num.append(num)

while True:
    #차가 막히는 시간대인지 확인하고자 시간을 구함.
    n = datetime.datetime.now()
    try:
        # 00시에는 csv파일을 생성한다.
        if(n.hour == 4) or (n.hour == 16):
            date = n.strftime('%Y%m%d')
            if n.hour == 4:
                output_file = output + str(date)+"_AM.csv"
            else:
                output_file = output + str(date) + "_PM.csv"
            header_list = [header]
            df = pd.DataFrame(header_list)
            df.to_csv(output_file, index=False, encoding='euc-kr')
            print("{} 파일이 생성되었습니다.".format(output_file))

        # 7~14시 or  15~22시 사이.
        #if True:
        if (n.hour > 6 and n.hour < 15) or (23 > n.hour and n.hour > 16 ) :

            for i in arr_num:
                elem = driver.find_element_by_id("nx_query")
                elem.clear()
                str_len = len(str(data_frame.iloc[i, 1]))
                busStop_no = ""
                if str_len < 5:
                    ea_zero = 5 - str_len
                    for k in range(0, ea_zero):
                        busStop_no += "0"
                busStop_no += str(data_frame.iloc[i, 1])
                busStop_name = str(data_frame.iloc[i, 2])
                elem.send_keys("부산 " + busStop_no)
                driver.find_element_by_xpath("//*[@id=\"nx_search_form\"]/fieldset/button").click()

                time.sleep(1)

                # 변수 설정
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                now = datetime.datetime.now()
                bus_arrive_information = []
                date = now.strftime('%Y/%m/%d %H:%M:%S')
                try:
                    #68번 버스를 찾는 과정
                    for i in range(0, len(soup.find_all("a", {'class': 'place_num'}))):
                        bus_no_list = soup.find_all("a", {'class': 'place_num'})[i].string
                        #print(bus_no_list)
                        if bus_no_list == '68':
                            bus_no = bus_no_list
                            count = i


                    # 현재 페이지에 다양한 em태그들이 있어서 예상 시간 추출이 어려움.
                    # 부분적으로 hmtl 코드를 가져와서 em태그를 찾아 출력하는 방식
                    test = soup.find_all("span", {'class': "bus_line"})[count]
                    print(test)
                    test = test.prettify()
                    soup2 = BeautifulSoup(test, 'html.parser')
                    predict_bus_arrive = str(soup2.find("em").string)
                    predict_bus_arrive = predict_bus_arrive.strip()
                    print(predict_bus_arrive)
                except:
                    predict_bus_arrive = "도착정보 없음"

                #csv파일에 넣기 위해 배열을 만듦.
                bus_arrive_information = [busStop_no, busStop_name, bus_no, predict_bus_arrive, str(date)]
                column_index = []


                #csv파일에 얻은 정보를 추가.
                with open(output_file, 'a') as csv_out_file:
                    filewriter = csv.writer(csv_out_file)
                    row_index = []
                    for index_value in range(len(header)):
                        column_index.append(index_value)
                        print(bus_arrive_information[index_value])
                        row_index.append(bus_arrive_information[index_value])
                    filewriter.writerow(row_index)

        else:
            print(n)
            print("30분 후에 다시 실행.")
            time.sleep(1800)
    except Exception as e:
        print("오류발생")
        print(e)