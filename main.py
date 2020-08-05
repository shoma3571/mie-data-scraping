from urllib import request  # urllib.requestモジュールをインポート
from bs4 import BeautifulSoup  # BeautifulSoupクラスをインポート
import json
import re
import datetime

url = 'https://www.pref.mie.lg.jp/YAKUMUS/HP/m0068000066_00002.htm'
table_url = 'https://www.pref.mie.lg.jp/YAKUMUS/HP/m0068000066_00011.htm'
table_response = request.urlopen(table_url)
table_soup = BeautifulSoup(table_response,'html.parser')
response = request.urlopen(url)
soup = BeautifulSoup(response,'html.parser')


# 配列を定義する
# 感染者のデータ
infected_persons_data = []

# 検査件数のデータ
num_of_inspections = []

# 陽性者数のデータ
num_of_infected_persons = []

trans_table = str.maketrans({"０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9",})

# 感染者データの取得
# dataがテーブル丸ごとを取得
all_table = table_soup.find('table',class_='undefined')
# theadを抜いた部分
tbody = all_table.find('tbody')
# tr属性を全取得
tr = tbody.find_all('tr')

# tr属性の回数だけループ
for item in tr:
    date = ''
    city = ''
    age = ''
    gender = ''
    date_relese = "T00:00:00.000Z"

    tr_data = item.find_all('td')

    for i in range(len(tr_data)):
        if i==1:
            date_ = tr_data[i].text
            date_ = date_.translate(trans_table)
            m = re.findall(r"\d+", date_)
            d = datetime.datetime(2020, int(m[0]), int(m[1]))
            date = d.strftime("%Y-%m-%d")
            date_relese = date + date_relese
            
        if i==2:
            city = tr_data[i].text

        if i==3:
            age_ = tr_data[i].text
            age = age_.translate(trans_table)
            
        if i==4:
            gender = tr_data[i].text

    infected_persons_data.append({
        "リリース日":date_relese,
        "居住地":city,
        "年代":age,
        "性別":gender,
        "date":date
    })


# 検査件数、陽性者数データの取得
div = soup.find('div',id='article')
out_table = div.find('table')
out_tbody = out_table.find('tbody')
out_tr = out_tbody.find('tr')
out_td = out_tr.find('td')
inner_table = out_td.find('table')
# theadを抜いた部分
inner_tbody = inner_table.find('tbody')
# tr属性を全取得
inner_tr = inner_tbody.find_all('tr')

# tr属性の回数だけループ
for item in inner_tr:
    ip_date = ''
    i_date = ''
    inspections = 0
    infected_person = 0

    tr_data = item.find_all('td')

    for i in range(len(tr_data)):
        if i==0:
            date_ = tr_data[i].text
            date_ = date_.translate(trans_table)
            m = re.findall(r"\d+", date_)
            d = datetime.datetime(2020, int(m[0]), int(m[1]))
            date = d.strftime("%Y-%m-%d")
            ip_date= date+'T08:00:00.000+09:00'
            i_date = date+'T18:00:00.000+09:00'
        if i==1:
            inspections = int(tr_data[i].text)
        if i==2:
            infected_person = int(tr_data[i].text)
    
    num_of_inspections.append({'日付':i_date,'小計':inspections})
    num_of_infected_persons.append({'日付':ip_date,'小計':infected_person})
        







response.close()
infected_persons_data.reverse()
num_of_infected_persons.reverse()
num_of_inspections.reverse()



data_dict_of_infected_persons_data = {
    "date":'hoge',
    "data":infected_persons_data
}

data_dict_of_infected_persons = {
    "date":'hoge',
    "data":num_of_infected_persons
}

data_dict_of_inspections ={
    "date":'hoge',
    "data":num_of_inspections
}

with open('infected_person_data.json',mode='w',encoding='utf-8') as f:
    
    f.write(json.dumps(data_dict_of_infected_persons_data,ensure_ascii = False,indent = 4))

with open('infected_person.json',mode='w',encoding='utf-8') as f:
    
    f.write(json.dumps(data_dict_of_infected_persons,ensure_ascii = False,indent = 4))

with open('Number_of_inspections.json',mode='w',encoding='utf-8') as f:
    
    f.write(json.dumps(data_dict_of_inspections,ensure_ascii = False,indent = 4))