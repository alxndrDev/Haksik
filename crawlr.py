import requests
from bs4 import BeautifulSoup
import datetime

url = "http://www.kopo.ac.kr/incheon/content.do?menu=6893"
header = {'user-agent': ''}
response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, 'html.parser') #html.parser를 사용해서 soup에 넣겠다.

contents = soup.select('.tbl_table tbody tr')

c =[]

for i in range(1,6):
    a = contents[i].get_text().strip('\n').split('\n')
    c.append([x for x in a if x])
when = ['월','화','수','목','금',]
for j in range(0,len(c)):
    for i in range(0,4):
        if i == 0:
            c[j][i] = when[j]+"/"+str(datetime.date.today() + datetime.timedelta(days=j))
        print(c[j][i])
        print("*"*50)