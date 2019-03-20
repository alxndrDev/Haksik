import requests
from bs4 import BeautifulSoup


url = "http://www.kopo.ac.kr/incheon/content.do?menu=6893"
header = {'user-agent': ''}
response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, 'html.parser') #html.parser를 사용해서 soup에 넣겠다.

contents = soup.select('.tbl_table tbody tr')

print(type(contents))
c =[]
for i in range(1,5):
    a = contents[i].get_text().strip('\n').split('\n')

    c.append([x for x in a if x])


for j in c:
    for i in j:
        print(i)
    print("*"*50)