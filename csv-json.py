import sys
import pandas as pd
import csv
import json

print(sys.argv[1])

df = pd.read_csv(sys.argv[1])
vals=df.iloc[:,:].values.tolist()
print(len(vals))
headers = pd.read_csv(sys.argv[1], nrows=1).columns.values.tolist()
print(len(headers))

list=[]
dict={}

for i in range(0,len(vals)):
    for j in range(0,len(headers)):
        dict[headers[j]]=vals[i][j]
    list.append(dict)
    dict={}
    
#print(list)

with open('./files/jsonfile.json', 'w') as fp:
    json.dump(list, fp)
    

