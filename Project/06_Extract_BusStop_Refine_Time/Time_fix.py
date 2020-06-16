#!/usr/bin/env python3

import pandas as pd
import csv

arr_bus = ['17','40','68','81', '138-1']
arr_time = ['AM','PM']
header = ['BusStop_No','Bus_No','Predict_Arrive','Date','hour','min','sec']

for num in arr_bus:
    for time_set in arr_time:
        input_file = 'csv/Extract_Refine_by' + num + '_' + time_set + '.csv'
        output_file = "fix/time_fix_by" + num +'_' + time_set + '.csv'
        fix_arr = pd.DataFrame([header])
        fix_arr.to_csv(output_file, index=False, encoding='utf-8')
        print("{} 파일이 생성되었습니다.".format(output_file))

        #print(fix_arr)
        data_frame = pd.read_csv(input_file)
        for i in range(0,len(data_frame)):
            #data_frame.loc[i, ['BusStop_No', 'Bus_No', 'Predict_Arrive']]
            BS_no = (data_frame.loc[[i], ['BusStop_No']].values[0])[0]
            B_no = (data_frame.loc[[i], ['Bus_No']].values[0])[0]
            pred = (data_frame.loc[[i], ['Predict_Arrive']].values[0])[0]
            timeing = (data_frame.loc[[i],['Current_Time']].values[0])[0].split()
            date = timeing[0]
            hour = (timeing[1].split(":"))[0]
            min = (timeing[1].split(":"))[1]
            sec = (timeing[1].split(":"))[2]


            # csv파일에 넣기 위해 배열을 만듦.
            columns = [BS_no,B_no,pred,date,hour,min,sec]
            print(columns)
            column_index = []

            # csv파일에 얻은 정보를 추가.
            with open(output_file, 'a') as csv_out_file:
                filewriter = csv.writer(csv_out_file)
                row_index = []
                for index_value in range(len(header)):
                    column_index.append(index_value)
                    print(columns[index_value])
                    row_index.append(columns[index_value])
                filewriter.writerow(row_index)