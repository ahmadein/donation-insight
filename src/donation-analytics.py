import pandas as pd
import numpy as np

def read_filter_with_pandas(filename, df_index_to_keep):
    df = pd.read_csv(filename, delimiter='|', header=None)
    df_filtered = df[df_index_to_keep]
    return df_filtered


filename='../input/itcont.txt'
df_index_to_keep =[0,7,10,13,14,15]
df = read_filter_with_pandas(filename, df_index_to_keep)
df.columns = ['CMTE_ID','NAME','ZIP_Code','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
print(df[0])
