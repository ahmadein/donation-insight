import numpy as np
import argparse
import time
import sys
start_time = time.time()
# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-in", "--input_file", metavar="FILE NAME", required=False, default='../input/itcont.txt', help="enter input file path")
parser.add_argument("-per", "--percentile_file", metavar="FILE NAME", required=False, default='../input/percentile.txt', help="enter percentile file path")
parser.add_argument("-out", "--out_file", metavar="FILE NAME", required=False, default='../output/repeat_donors.txt', help="enter output file path")
args = parser.parse_args()
print(args)
filename = args.input_file
percentile_filename = args.percentile_file
out_file_name = args.out_file
columns_header = {'CMTE_ID': 0, 'NAME': 7, 'ZIP_CODE': 10, 'TRANSACTION_DT': 13, 'TRANSACTION_AMT': 14, 'OTHER_ID': 15}  # default dictionary for which columns to read
index_to_keep = [columns_header['CMTE_ID'], columns_header['NAME'], columns_header['ZIP_CODE'], columns_header['TRANSACTION_DT'], columns_header['TRANSACTION_AMT'], columns_header['OTHER_ID']]
# order of processing by default 0,7,10,13,14,15
cmte_id_dict = {}
donor_list = {}
line_number = 0
foutobj = open(out_file_name, 'w')  # open out file and get it ready for writing
with open(percentile_filename, 'r') as f:  # get the percentile value to be calculated
    percentile_value = int(f.read())
with open(filename) as f:
    for line in f:  # read from input file line by line
        line_number += 1
        if line_number % 10000 == 0:
            print('processing line number ' + str(line_number))

        data_txt = line.split('|')
        if(data_txt[columns_header['CMTE_ID']] == '' or data_txt[columns_header['NAME']] == '' or data_txt[columns_header['ZIP_CODE']] == ''
            or len(data_txt[columns_header['ZIP_CODE']]) < 5 or data_txt[columns_header['TRANSACTION_DT']] == '' or
                data_txt[columns_header['TRANSACTION_AMT']] == '' or data_txt[columns_header['OTHER_ID']] != ''):
            continue  # if line is invalid or other ID has value, get the next line
        filtered_data = [data_txt[i] for i in index_to_keep]
        filtered_data[2] = filtered_data[2][:5]  # first 5 charachters of zip code
        filtered_data[4] = round(float(filtered_data[4]))
        zip_code = filtered_data[2]
        uniq_donor_id = filtered_data[1]+zip_code  # combine donor name and zipcode to form unique donor id
        year = int(filtered_data[3][-4:])
        if uniq_donor_id not in donor_list:  # find if donor was repeated
            donor_list[uniq_donor_id] = year  # if new donor, add calendar year to ignore next occurance if not in correct order
            continue
        elif year >= donor_list[uniq_donor_id]:
            donor_list[uniq_donor_id] = year  # repeated donor found and year is in order
            try:
                _element = cmte_id_dict[filtered_data[0]][zip_code][year]  # test if a record for same triplets (committee, zip, year) exist
            except KeyError:
                cmte_id_dict[filtered_data[0]] = {zip_code: {year: {'value': [filtered_data[4]], 'repeated': 1}}}  # initialize
                data_to_write = [filtered_data[0], zip_code, year, np.percentile(cmte_id_dict[filtered_data[0]][zip_code][year]['value'], percentile_value, interpolation='nearest'),
                                 cmte_id_dict[filtered_data[0]][zip_code][year]['value'][0], cmte_id_dict[filtered_data[0]][zip_code][year]['repeated']]
                foutobj.write('|'.join(str(i) for i in data_to_write)+'\n')  # write in the file for the first record found
                continue
            cmte_id_dict[filtered_data[0]][zip_code][year]['value'].append(filtered_data[4])  # add donation value to list of existing donations
            cmte_id_dict[filtered_data[0]][zip_code][year]['repeated'] += 1
            data_to_write = [filtered_data[0], zip_code, year, np.percentile(cmte_id_dict[filtered_data[0]][zip_code][year]['value'], percentile_value, interpolation='nearest'),
                             int(np.sum(cmte_id_dict[filtered_data[0]][zip_code][year]['value'])), cmte_id_dict[filtered_data[0]][zip_code][year]['repeated']]
            foutobj.write('|'.join(str(i) for i in data_to_write)+'\n')
foutobj.close()
print('done with number of line ' + str(line_number))
print("--- %s seconds ---" % (time.time() - start_time))
print('sizes of dicts')
print(sys.getsizeof(uniq_donor_id), sys.getsizeof(cmte_id_dict))