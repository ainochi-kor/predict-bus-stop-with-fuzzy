#!/usr/bin/env python3

import pandas as pd
import os

arr_bus = ['17','40','68', '81', '138-1']
arr_time = ['AM','PM']
header = ['BusStop_No','Bus_No','Predict_Arrive','Date','hour','min','sec']

for num in arr_bus:
    for time in arr_time:
        input_file = 'csv/Extract_Refine_by' + num + '_' + time + '.csv'
        output_file = "fix/time_fix_by" + num +'_' + time + '.csv'
        fix_arr = [header]
        #print(fix_arr)
        data_frame = pd.read_csv(input_file)
        for i in range(0,len(data_frame)):
            columns = []
            #data_frame.loc[i, ['BusStop_No', 'Bus_No', 'Predict_Arrive']]
            BS_no = (data_frame.loc[[i], ['BusStop_No']].values[0])[0]
            B_no = (data_frame.loc[[i], ['Bus_No']].values[0])[0]
            pred = (data_frame.loc[[i], ['Predict_Arrive']].values[0])[0]
            time = (data_frame.loc[[i],['Current_Time']].values[0])[0].split()
            date = time[0]
            hour = (time[1].split(":"))[0]
            min = (time[1].split(":"))[1]
            sec = (time[1].split(":"))[2]
            all_data = [BS_no,B_no,pred,date,hour,min,sec]
            fix_arr.append(all_data)
            print(all_data)
        print(fix_arr)
        fix_arr.to_csv(output_file, index=False)