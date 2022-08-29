import requests 
from bs4 import BeautifulSoup
import pandas as pd 

path = './Hosts arcanum - tz AOS 2k.html' 
soup = BeautifulSoup(open(path, encoding="utf8"), "html.parser")
#  <li class="category">
categories = soup.find_all('li', class_='category')
outputFolder = './output'
arr = [] 
for cat in categories : 

    cat_title = cat.find('h3').get_text()

    selects = cat.find_all( 'li' , class_ ="rootselection" ) 
    for s in selects : 
        json = {} 
        json['category_title'] = cat_title 
        json['select_name'] = s.find('h4').get_text()
        n =  json['select_name']
        json['name_clean'] = n 
        leftBracketIndex = n.rfind('[')
        rightBracketIndex = n.rfind(']')
        if leftBracketIndex != -1:
            pts = n[ leftBracketIndex + 1 : rightBracketIndex ].replace('pts', '')
            json['points'] = pts 
            json['name_clean'] = n[ 0 : leftBracketIndex -1 ]
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
            tableName = json['name_clean'] + '_' + listHeaders[0].get_text()
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
            sTable_df.to_csv ( f"{outputFolder}//{tableName}.csv" , index=False )
                    
            #print ( tableName )
            tableName = 'REPLACE_ME'

            
        arr.append( json )
    #arr.append( json )

df = pd.DataFrame( arr ) 
oPath =  f"./{outputFolder}/battlescribe_export.csv"
df.to_csv(oPath , index=False)
print('output to ' , oPath )
#print(len(categories))
#period = tonight.find(class_="period-name").get_text()

