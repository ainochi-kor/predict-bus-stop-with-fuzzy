#!/usr/bin/env python3

import pandas as pd
import csv

arr_bus = ['138-1']
arr_time = ['AM','PM']
header = ['BusStop_No','Bus_No','Predict_Arrive','Date','hour','min','sec','stop hour','stop min']

for num in arr_bus:
    for time_set in arr_time:
        input_file = 'fix/time_fix_by' + num +'_' + time_set + '.csv'
        output_file = 'mad/missing_and_diet_by' + num +'_' + time_set + '.csv'
        mad_arr = pd.DataFrame([header])
        mad_arr.to_csv(output_file, index=False, encoding='utf-8')
        print("{} 파일이 생성되었습니다.".format(output_file))

        print(input_file)
        data_frame = pd.read_csv(input_file, header = [1], index_col=None , encoding='euc-kr')
        #print(data_frame)
        data_frame = data_frame.drop_duplicates(['BusStop_No','Date','hour','min'])

        for row in range(0,len(data_frame)):

            c_min = data_frame.iloc[row][5]
            c_hour = data_frame.iloc[row][4]
            try:
                if data_frame.iloc[row][2] != '도착정보 없음':
                    p_min = int(data_frame.iloc[row][2].replace('분', ''))
                else:
                    p_min = 0
                stop_min = c_min + p_min
                stop_hour = c_hour
                if stop_min > 59:
                    stop_min -= 60
                    stop_hour += 1

                # data_frame.iloc[row][7] = stop_hour
                # data_frame.iloc[row][8] = stop_min
                frame = data_frame.iloc[row]
                new_data_frame = [frame[0],frame[1],frame[2],frame[3],frame[4]\
                    ,frame[5],frame[6], stop_hour, stop_min]
                column_index = []

                # csv파일에 얻은 정보를 추가.
                with open(output_file, 'a') as csv_out_file:
                    filewriter = csv.writer(csv_out_file)
                    row_index = []
                    for index_value in range(len(header)):
                        column_index.append(index_value)
                        #print(new_data_frame[index_value])
                        row_index.append(new_data_frame[index_value])
                    filewriter.writerow(row_index)
            except:
                print("다음")