# FuzzyPredictBusStop
버스 정류장 예상 도착시간의 예측 향상을 위해 퍼지 알고리즘을 이용한 프로젝트. 

<br><br><br>
## [01_Bus_Location]
: 해당 시간의 해당 번호의 버스들의 위치를 파악하여 크롤링하여 CSV파일에 버스 번호, 현재 위치, Date를 추가한다.

<br><br>
## [02_Bus_Stop]
: 해당 버스 번호의 버스 정류장 경로 정보에서 버스 정류장의 번호와 정류장 이름을 CSV파일에 저장한다.

<br><br>
## [03_BusStop_Refine]
:  02에서 추출한 CSV파일 중 정류장 번호가 없는 행을 제거하고, 정류장 사이의 '-'문자를 제거하여 다시 CSV파일로 정제한다.

<br><br>
## [04_BusStop_Infomation]
: 03에서 정제한 버스 정류장 파일을 이용하여, 원하는 정류장을 정한 뒤, 해당 버스 정류장의 원하는 버스의 도착 예정시간을 크롤링하여 CSV파일로 저장

<br><br>
## [05_Extract_BusStop_Refine_Sum]
: 04에서 추출한 모든 CSV파일 중 '버스 번호의 오전or오후'를 하나로 통합한다.

<br><br>
## [06_Extract_BusStop_Refine_Time]
: 05의 CSV파일의 Date의 년월일시분초를 년월일, 시, 분, 초로 나누어서 다시 저장하도록 한다.

<br><br>
## [07_Extract_BusStop_Refine_MissingDataAndDataDiet]
: 06의 CSV파일 중 결측행을 제거하고, '정류장 번호,날짜,시간,분'을 기준으로 데이터를 줄이도록 한다.   

<br><br>
## [08_Sort_BusStop_Data]
: 07의 데이터를 정류장 별로 데이터를 정렬하도록 한다.

<br><br>
## [09_Fuzzy_Bus_Stop]
: 08폴더에서 가져온 CSV파일을 기초로 한다. 이 프로그램은 퍼지 알고리즘을 이용하여 버스 정류장과 시간을 입력하면 지연시간을 계산하여, 예정 도착 시간을 알려주도록 한다.
