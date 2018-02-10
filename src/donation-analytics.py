import csv
'''
import pandas as pd
def read_filter_with_pandas(filename, df_index_to_keep):
    df = pd.read_csv(filename, delimiter='|', header=None)
    df_filtered = df[df_index_to_keep]
    return df_filtered
'''

filename = '../input/itcont_example.txt'
out_file_name = '../output/repeat_donors.txt'
df_index_to_keep =[0,7,10,13,14,15]
columns_header = {'CMTE_ID': 0, 'NAME': 7, 'ZIP_CODE': 10, 'TRANSACTION_DT': 13, 'TRANSACTION_AMT': 14, 'OTHER_ID': 15}
#df = read_filter_with_pandas(filename, df_index_to_keep)
cmte_id_dict={}
donor_list = {}
line_number = 0
foutobj = open(out_file_name,'w')
with open(filename) as f:
    for line in f:
        line_number +=1
        data_txt=line.split('|')
        if(data_txt[columns_header['CMTE_ID']]=='' or data_txt[columns_header['NAME']]=='' or data_txt[columns_header['ZIP_CODE']]==''
            or len(data_txt[columns_header['ZIP_CODE']])<5 or data_txt[columns_header['TRANSACTION_DT']]=='' or
                data_txt[columns_header['TRANSACTION_AMT']]=='' or data_txt[columns_header['OTHER_ID']]!=''):
            continue
        filtered_data=[data_txt[i] for i in df_index_to_keep]
        filtered_data[2] = filtered_data[2][:5] # first 5 charachters of zip code
        zip_code=filtered_data[2]
        uniq_donor_id = uniq_donor_id = filtered_data[1]+filtered_data[2]
        year = int(filtered_data[3][-4:])
        if uniq_donor_id not in donor_list:
            donor_list[uniq_donor_id] = year
            continue
        elif year >= donor_list[uniq_donor_id]:
            donor_list[uniq_donor_id] = year #repeated donor found and year is in order
            try:
                _element = cmte_id_dict[filtered_data[0]][zip_code][year] # test if a record for same tuple (committee, zip, year) exist
            except KeyError:
                cmte_id_dict[filtered_data[0]] = {zip_code: {year: {'value': int(filtered_data[4]), 'repeated': 1}}}
                data_to_write = [filtered_data[0], zip_code, year, line_number, cmte_id_dict[filtered_data[0]][zip_code][year]['value'], cmte_id_dict[filtered_data[0]][zip_code][year]['repeated']]
                foutobj.write('|'.join(str(i) for i in data_to_write)+'\n') # write in the file for the first record found
                continue
            cmte_id_dict[filtered_data[0]][zip_code][year]['value'] += int(filtered_data[4])
            cmte_id_dict[filtered_data[0]][zip_code][year]['repeated'] += 1
            data_to_write = [filtered_data[0], zip_code, year, line_number, cmte_id_dict[filtered_data[0]][zip_code][year]['value'], cmte_id_dict[filtered_data[0]][zip_code][year]['repeated']]
            foutobj.write('|'.join(str(i) for i in data_to_write)+'\n')
foutobj.close()
print('done with number of line' + str(line_number))


