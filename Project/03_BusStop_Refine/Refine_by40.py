import pandas as pd
import csv
import glob
import os

input_file = 'csv/busStop_by40.csv'
output_file = 'refine/busStop_Refine_by40.csv'

data_frame = pd.read_csv(input_file, encoding='euc-kr')

#정류장 번호가 없는 곳은 측정할 수 없기에 행을 지운다.
data_frame_drop = data_frame.dropna(axis=0)
data_frame_drop['num'] = data_frame_drop['num'].str.replace("-", "")
sample_data_frame = data_frame_drop.iloc[:,[1,2]]
print(sample_data_frame)

sample_data_frame.to_csv(output_file,encoding="euc-kr")