#!/usr/bin/env python3

import pandas as pd
import glob
import os

arr_bus = ['17','40','68', '81', '138-1']
arr_time = ['AM','PM']

for num in arr_bus:
    input_path = 'csv/busStop/busStop_by'+num
    for time in arr_time:
        all_files = glob.glob(os.path.join(input_path, \
            'information_predict_arrive_busStop_by'+ num +'*'+ time +'.csv'))
        output_file = 'csv/Extract_Refine_by' + num +"_"+time+'.csv'
        all_data_frames = []

        for input_file in all_files:
            data_frame = pd.read_csv(input_file ,header = 1,index_col=1,encoding="euc-kr")
            data_frame_drop = data_frame.dropna(axis=0)

            data_frame_drop['Current_Time'] = pd.to_datetime(data_frame_drop["Current_Time"])
            all_data_frames.append(data_frame_drop)

        # 결과를 출력합니다.
        print(all_data_frames)

        data_frame_concat = pd.concat(all_data_frames, axis=0, ignore_index=True)
        data_frame_concat.to_csv(output_file, index = False)