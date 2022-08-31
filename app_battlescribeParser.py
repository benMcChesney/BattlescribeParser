from pickle import FALSE, TRUE
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from os.path import exists
import csv


def clean_points_from_string ( input, key, json ):
    
    
    json[ key ] = input 
    n =  input
    leftBracketIndex = n.rfind('[')
    rightBracketIndex = n.rfind(']')
    if leftBracketIndex != -1:
        pts = n[ leftBracketIndex + 1 : rightBracketIndex ].replace('pts', '')
        json[ f"{key}_pts"] = pts 
        json[ key ] = n[ 0 : leftBracketIndex -1 ]

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
       



     
path = './Tzeentch AOS - current.html' 
soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
#  <li class="category">
categories = soup.find_all('li', class_='category')
outputFolder = './output'
arr = [] 
cleanDataArray = [] 
for cat in categories : 

    cat_title = cat.find('h3').get_text()

    selects = cat.find_all( 'li' , class_ ="rootselection" ) 
    for s in selects : 
        json = {} 
        clean_points_from_string( cat_title , 'category_title', json )
        #json['category_title'] = cat_title 
        json['select_name'] = s.find('h4').get_text()
        json['tags'] = s.find('p', class_="category-names").get_text()
        clean_points_from_string( json['select_name'] , 'select_name_clean', json )
        json['selections'] = s.find('p').get_text() #.replace(':', ':\n')
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
                    jr_value = _data.get_text()  
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

