import os
import csv

def write_csv(data):
    datas = {data}
    with open(os.getcwd()+'diary/applications/'+'data.csv','a') as f:
        write = csv.writer(f, lineterminator='\n')
        writer.writerow(datas)