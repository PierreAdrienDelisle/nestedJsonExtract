# -*- coding: utf-8 -*-

# Found code on https://github.com/vinay20045/json-to-csv
import sys
import numpy
import json
import csv
import pandas as pd
import os
##
# Convert to string keeping encoding in mind...
##
def to_string(s):
    try:
        return str(s)
    except:
        #Change the encoding type if needed
        return s.encode('utf-8')


##
# This function converts an item like
# {
#   "item_1":"value_11",
#   "item_2":"value_12",
#   "item_3":"value_13",
#   "item_4":["sub_value_14", "sub_value_15"],
#   "item_5":{
#       "sub_item_1":"sub_item_value_11",
#       "sub_item_2":["sub_item_value_12", "sub_item_value_13"]
#   }
# }
# To
# {
#   "node_item_1":"value_11",
#   "node_item_2":"value_12",
#   "node_item_3":"value_13",
#   "node_item_4_0":"sub_value_14",
#   "node_item_4_1":"sub_value_15",
#   "node_item_5_sub_item_1":"sub_item_value_11",
#   "node_item_5_sub_item_2_0":"sub_item_value_12",
#   "node_item_5_sub_item_2_0":"sub_item_value_13"
# }
##
def reduceItemRec(key, value):

    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduceItemRec(key+'_'+to_string(i), sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduceItemRec(key+'_'+to_string(sub_key), value[sub_key])

    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)
        
def reduceItemWithKey(key, value):
    global reduced_item

    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduceItemRec(key+to_string(i)+"_", sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduceItemRec(key+to_string(sub_key), value[sub_key])

    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)



if __name__ == "__main__":
    if len(sys.argv) != 6:
        print ("\nUsage: myscript.exe <node> <json_file_path> <path/to/out_filename> <csv/xlsx> <HeaderNode yes/no> \n")
        print ("\nFor example : nestedJsonExtract.exe releveListBean ../../file.json ../outputFile csv no \n")
    else:
        #Reading arguments
        node = sys.argv[1]
        json_file_path = sys.argv[2]
        filename = sys.argv[3]
        extension = sys.argv[4]
        headerNode = sys.argv[5]
        
        fp = open(json_file_path, 'r+')
        json_value = fp.read()
        raw_data = json.loads(json_value)
        fp.close()

        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data

        processed_data = []
        header = []

        for item in data_to_be_processed:
            reduced_item = {}
            if(headerNode == "yes"):
                reduceItemWithKey(node+"_", item)
            else:
                reduceItemWithKey("",item)

            header += reduced_item.keys()
            processed_data.append(reduced_item)

        header = list(set(header))
        header.sort()

        with open(filename+".csv", 'w+') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)

        read_file = pd.read_csv(filename+".csv")
        if(extension == "csv"):
            read_file.to_csv(filename+".csv", index = None, header=True)
            print("Successfully write csv file as "+filename+".csv")
        else:
            read_file.to_excel(filename+".xlsx", index = None, header=True)
            os.remove(filename+".csv")
            print("Successfully write xlsx file as "+filename+".xlsx")
