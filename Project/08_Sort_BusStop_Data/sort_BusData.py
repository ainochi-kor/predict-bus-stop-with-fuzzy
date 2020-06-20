#!/usr/bin/env python3
import csv
import pandas as pd

arr_bus = ['17','40','68','81', '138-1']
arr_time = ['AM','PM']
header = ['BusStop_No','Bus_No','Predict_Arrive','Date','hour','min','sec','stop hour','stop min']

for bus_num in arr_bus:
    #정류장의 csv파일을 가져옴.
    bus_stop_csv = 'refine/busStop_Refine_by' + bus_num + '.csv'
    busStop_df = pd.read_csv(bus_stop_csv, encoding='euc-kr')
    for time_set in arr_time:
        #정제한 파일의 정보를 가져옴.
        input_file = 'mad/missing_and_diet_by' + bus_num +'_' + time_set + '.csv'
        bus_info_df = pd.read_csv(input_file, header=[1], index_col=None, encoding='euc-kr')
        output_file = 'Sort/Sort_Bus_Data_by' + bus_num +'_' + time_set + '.csv'
        mad_arr = pd.DataFrame([header])
        mad_arr.to_csv(output_file, index=False, encoding='euc-kr')
        print("{} 파일이 생성되었습니다.".format(output_file))

        # p_min : predict min.
        for bus_stop_row in range(0,len(busStop_df)):
            #print(busStop_df.iloc[bus_stop_row][1])
            busStop = busStop_df.iloc[bus_stop_row][1]
            for row in range(0,len(bus_info_df)):
                bus_info_Stop = bus_info_df.iloc[row][0]
                #print(bus_info_df.iloc[row][0])
                if busStop == bus_info_Stop:
                    print(bus_info_df.iloc[row])
                    # csv파일에 얻은 정보를 추가.
                    column_index = []
                    with open(output_file, 'a') as csv_out_file:
                        filewriter = csv.writer(csv_out_file)
                        row_index = []
                        filewriter.writerow(bus_info_df.iloc[row])
            print(bus_info_Stop  + ", 다음")


