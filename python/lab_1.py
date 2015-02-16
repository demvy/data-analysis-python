__author__ = 'valeriy'

import pandas as pd
import urllib2
import datetime
import os


def change_id():
    id = [24, 25, 5, 6, 27, 23, 26, 7, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 8, 9, 10, 1, 3, 2, 4, 12]
    return id


def download_vhi_files():
    os.chdir('/home/valeriy/proga_2curs/python/VHI')
    formatation = '%Y-%m-%d %H:%M'
    for id in change_id():
        if id < 10:
            id = '0'+str(id)
        curr_time = datetime.datetime.now()
        time_string = curr_time.strftime(formatation)
        url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R"+str(id)+".txt"
        vhi_url = urllib2.urlopen(url)
        out = open('vhi_id_'+str(id)+' '+time_string+'.csv', 'wb')
        out.write(vhi_url.read())
        out.close()
        print "VHI "+str(id)+" is downloaded..."


def read_csv(path_to_dir):
    data = []
    for filename in os.listdir(path_to_dir):
        df = pd.read_csv(filename, index_col=False, header=1)
        data.append(df)
    return data


def print_vhi_year(data, id, year):
    province_data = data[id]
    list_1 = province_data.VHI[(province_data['year']==year) & (province_data['year'] != 0) &
                               (province_data['VHI'] > 0) & (province_data['week'] > 0) ].tolist()
    print 'VHI for province '+str(id)+' for the year '+str(year)
    print', '.join(str(x) for x in list_1)
    print 'max = ' + str(max(list_1))
    print 'min = ' + str(min(list_1))
    print


def print_vhi_extreme_drought(data, id, percent):
    province_data = data[id]
    list_1 = province_data.VHI[0:]
    print 'VHI for province ' + str(id)
    print ', '.join(str(x) for x in list_1)
    list_2 = province_data.year[(province_data['%Area_VHI_LESS_15'] < percent)].unique().tolist()
    print 'years with extreme drought(less than '+str(percent)+'):'
    print ', '.join(str(x) for x in list_2)
    print

def print_vhi_temperate_drought(data, id, percent):
    province_data = data[id]
    list_1 = province_data.VHI[0:]
    print 'VHI for province ' + str(id)
    print ', '.join(str(x) for x in list_1)
    list_2 = province_data.year[(province_data['%Area_VHI_LESS_35'] < percent) & (province_data['year'] > 0)
    ].unique().tolist()
    print 'years with temperate drought(less than '+str(percent)+'):'
    print ', '.join(str(x) for x in list_2)
    print


os.chdir('/home/valeriy/proga_2curs/python/VHI')
path = os.getcwd()
#download_vhi_files()
data = read_csv(path)
print_vhi_year(data, 13, 1994)
print_vhi_extreme_drought(data, 13, 0.02)
print_vhi_temperate_drought(data, 13, 0.02)
