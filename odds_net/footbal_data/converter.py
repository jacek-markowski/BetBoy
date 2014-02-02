# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:18:19 2013

@author: jacek
"""
from csv import reader
import os

class DataConverter(object):
    def __init__(self):
        pass
    def check_index_odds(self,csv):
        csv_file = reader(open(csv,'r'))
        number = 0
        for i in csv_file:
            for name in i:
                if 'B365H' == name:
                    print i[number],number,csv
                    index = number
                number += 1
        return index
    def fix_date(self,date):
        #print date,'<'
        day,month,year = date.split('/')
        if int(year) > 0 and int(year) < 30 and len(year)<4:
            year = 2000 + int(year)
        elif int(year) <= 99  and len(year)<4:
            year = 1900 + int(year)
        new_date = str(year)+'.'+month+'.'+day
        return new_date
    def convert(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f != 'converter.py':
                idx = self.check_index_odds(f) # odds index
                csv_file = reader(open(f,'r'))
                out_file = open(os.path.join('converted','')+f,'w')
                print f
                for i in csv_file:
                    if i[1] == 'Date':
                        pass
                    if i[1] != 'Date' and len(i[1])>7 and len(i[idx])>0:
                        print i[idx],'<'
                        date = self.fix_date(i[1])
                        odd_1 = float(i[idx])
                        odd_x = float(i[idx+1])
                        if odd_x < 2.95:
                            odd_x = 2.95
                        odd_2 = float(i[idx+2])
                        if odd_2 < 1:
                            odd_2 = 1
                        if odd_1 < 1:
                            odd_1 = 1
                        if odd_1<1:
                            odd_1=1
                        if odd_x<1:
                            odd_x=1
                        if odd_2<1:
                            odd_2=1
                        line = date+','+i[2]+','+i[3]+','+i[4]+','+i[5]+','+\
                            str(odd_1)+','+str(odd_x)+','+str(odd_2) # odds
                        out_file.write(line+'\n')
                out_file.close()


x = DataConverter()
x.convert()