from pickle import FALSE, TRUE
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from os.path import exists
import csv
import os 

import sys


def clean_points_from_string ( input ):
    copy =  input
    leftBracketIndex = copy.rfind('[')
    rightBracketIndex = copy.rfind(']')
    if leftBracketIndex != -1:
        str_replace = copy[ 0 : leftBracketIndex -1 ]
        str_replace = str_replace.replace(':', ' -')
        return str_replace
    return copy

def get_points_from_string ( input ):
    copy =  input
    leftBracketIndex = copy.rfind('[')
    rightBracketIndex = copy.rfind(']')
    if leftBracketIndex != -1:
        pts = copy[ leftBracketIndex + 1 : rightBracketIndex ].replace('pts', '')
        return pts
    return ""

def check_path ( new_path ):

    if exists(new_path):
        # path found, iterate until the
        writeIndex = 1 ; 
        while True :
            path_no_extension = new_path[0:-3]
            path = f"{path_no_extension}[{writeIndex}].csv"
            writeIndex += 1
            #print('trying ... ', path , exists(path) )
            if exists(path) == False : 
                return path ; 
    else :
        # use break to escape 
        # print('path does not exist!', new_path )
        return f"{new_path}"
       



     
path = './Tzeentch AOS - next2.html' 
if len( sys.argv) > 1 :
    path = sys.argv[1]
    print( f"loading html @ {path} ")


soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
#  <li class="category">
categories = soup.find_all('li', class_='category')
outputFolder = './output'
for f in os.listdir(outputFolder):
    os.remove(os.path.join(outputFolder, f))

arr = [] 
cleanDataArray = [] 
for cat in categories : 

    cat_title = cat.find('h3').get_text()

    selects = cat.find_all( 'li' , class_ ="rootselection" ) 
    for s in selects : 
        json = {} 
        json['category_title'] = clean_points_from_string( cat_title )
        json['category_title_pts'] = get_points_from_string( cat_title )
        #json['category_title'] = cat_title 
        nodeName = "REPLACE_NODE"
        if s.find('h3') != None :
            nodeName =  s.find('h3').get_text()
        if s.find('h4') != None :
            nodeName = s.find('h4').get_text()
        json['select_name'] = nodeName
        
        json['tags'] = s.find('p', class_="category-names").get_text()
        json['select_name_clean'] = clean_points_from_string( nodeName )
        json['select_name_clean_pts'] = get_points_from_string( nodeName )
        json['selections'] = s.find('p').get_text() #.replace(':', ':\n')
        json['profile_names'] = s.find('p',  class_="category-names").get_text()
        # don't need this, just parse the tables- better data 
        #pn = s.find('p' , class_ ="profile-names")
        #if pn != None:
        #   json['profile_name'] = pn.get_text().replace(':', ':\n')

        sTables = s.find_all( 'table')
        # each of these tables is a one-off, exported to a CSV 
        for t in sTables : 
            tableName = 'REPLACE_ME'
            listHeaders = list( t.find_all( 'th') ) 
            tableName = json['select_name_clean'] + '_' + listHeaders[0].get_text() + '_table'
            data_array = [] ; 
            sTable_df = None 
            # need to just get the text from each <th> tag 
            headers = [] 
            for h in listHeaders : 
                headers.append( h.get_text() )
                #print( 'adding' , h.get_text() )
            
            
            
            tr = t.find_all( 'tr' )
            for row in tr : 
                json_row = {} 
                td = row.find_all('td') 

                dataIndex = 0 
                for _data in td : 
                    #print('@ a row')
                    jr_key = headers[ dataIndex ]
                    # clean extra characters that mess up CSV export
                    jr_value = _data.get_text().replace( ',' , '')
                    jr_value = jr_value.replace("\\r", '')
                    jr_value = jr_value.replace("\\t", '')
                    #jr_value = jr_value.replace("\\n", '')
                    jr_value = jr_value.replace('    ', '')
                    jr_value = jr_value.replace( '''. 
''', '')
                    jr_value = jr_value.replace( '''.
''' , '' )
                    #jr_value = jr_value.replace('''
#''', '')
                    #jr_value = jr_value.replace('•', '|')

                    
                    json_row[ jr_key ] = jr_value 
                    

                    dataIndex += 1 
                
                # print( json_row )
                # ignore header row
                if len(td) > 0 :
                    data_array.append(json_row)

         
            sTable_df = pd.DataFrame( data_array ); 
            path = check_path( f"{outputFolder}/{tableName}.csv" ) 
            sTable_df.to_csv ( path , index=False )
            print( 'writing file out to ' , path )
                    
            #print ( tableName )
            tableName = 'REPLACE_ME'

            
        arr.append( json )
    #arr.append( json )

df = pd.DataFrame( arr ) 
oPath =  f"{outputFolder}/battlescribe_export.csv"
oPath_checked = check_path( oPath )
#df.to_csv(oPath_checked , index=False)
df.to_csv(oPath_checked , index=False)
print('output to ' , oPath_checked )
#print(len(categories))
#period = tonight.find(class_="period-name").get_text()

