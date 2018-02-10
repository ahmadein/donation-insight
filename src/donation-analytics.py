import pandas as pd
import numpy as np

def read_filter_with_pandas(filename, df_index_to_keep):
    df = pd.read_csv(filename, delimiter='|', header=None)
    df_filtered = df[df_index_to_keep]
    return df_filtered


filename='../input/itcont_example.txt'
df_index_to_keep =[0,7,10,13,14,15]
columns_header = {'CMTE_ID': 0, 'NAME': 7, 'ZIP_CODE': 10, 'TRANSACTION_DT': 13, 'TRANSACTION_AMT': 14, 'OTHER_ID': 15}
#df = read_filter_with_pandas(filename, df_index_to_keep)
cmte_id_dict=[]
donor_list = []
with open(filename) as f:
    for line in f:
        data_txt=line.split('|')
        if(data_txt[columns_header['CMTE_ID']]=='' or data_txt[columns_header['NAME']]=='' or data_txt[columns_header['ZIP_CODE']]==''
            or len(data_txt[columns_header['ZIP_CODE']])<5 or data_txt[columns_header['TRANSACTION_DT']]=='' or
                data_txt[columns_header['TRANSACTION_AMT']]=='' or data_txt[columns_header['OTHER_ID']]!=''):
            continue
        filtered_data=[data_txt[i] for i in df_index_to_keep]
        filtered_data[3] = filtered_data[3][:5] # first 5 charachters of zip code
        uniq_donor_id = uniq_donor_id = filtered_data[1]+filtered_data[3]
        if(uniq_donor_id not in donor_list):
            donor_list.append(uniq_donor_id)
            continue
        else:
            data_txt
