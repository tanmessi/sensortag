import csv
import pandas as pd
import numpy as np
from pandas import DataFrame #write
data = pd.read_csv("sensor.csv" , encoding='utf-8',  sep=',')
print(data)
ty = data['tAccX'].str.replace("(", "")
ty1 = data[' tAccZ'].str.replace(")", "")
ty2 = data[' tAccY']
data['tAccX'] = ty
data[' tAccZ'] = ty1
data[' tAccY'] = ty2


df = DataFrame(data, columns= ['tAccX', ' tAccY', ' tAccZ'])
export_csv = df.to_csv (r'writedatai.csv', index = None, header=True) # here you have to write path, where result file will be stored
print (df)
